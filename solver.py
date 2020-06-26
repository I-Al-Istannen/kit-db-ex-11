import csv
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List


@dataclass
class Rental:
    rental_id: int
    rental_date: date
    inventory_id: int
    customer_id: int
    return_date: date
    film_rental_duration: int
    film_rental_rate: float
    film_replacement_cost: float


@dataclass
class FilmInfo:
    inventory_id: int
    film_rental_duration: int
    film_rental_rate: float
    film_replacement_cost: float


@dataclass
class Payment:
    payment_id: int
    customer_id: int
    rental_id: int
    amount: float
    payment_date: date


def read_rentals(rental_path: Path, film_info_path: Path) -> List[Rental]:
    rentals: List[Rental] = []
    film_infos: Dict[int, FilmInfo] = {}

    with open(film_info_path) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
        for row in list(reader)[1:]:
            row = [x.strip() for x in row]
            inv_id = int(row[0])
            film_infos[inv_id] = FilmInfo(
                inventory_id=inv_id,
                film_rental_duration=int(row[1]),
                film_rental_rate=float(row[2]),
                film_replacement_cost=float(row[3])
            )

    with open(rental_path) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
        for row in list(reader)[1:]:
            row = [x.strip() for x in row]
            inventory_id = int(row[2])
            film_info = film_infos[inventory_id]
            rentals.append(Rental(
                rental_id=int(row[0]),
                rental_date=datetime.fromisoformat(row[1]).date(),
                inventory_id=inventory_id,
                customer_id=int(row[3]),
                return_date=datetime.fromisoformat(row[4]).date(),
                film_rental_duration=film_info.film_rental_duration,
                film_rental_rate=film_info.film_rental_rate,
                film_replacement_cost=film_info.film_replacement_cost
            ))

    return rentals


def read_payments(path: Path) -> List[Payment]:
    payments: List[Payment] = []

    with open(path) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t', quotechar='|')
        for row in list(reader)[1:]:
            row = [x.strip() for x in row]
            payments.append(Payment(
                payment_id=int(row[0]),
                customer_id=int(row[1]),
                rental_id=int(row[3]),
                amount=float(row[4]),
                payment_date=datetime.fromisoformat(row[5]).date()
            ))

    return payments


def filter_payments(payments: List[Payment]) -> List[Payment]:
    return [payment for payment in payments if payment.payment_date <= date.fromisoformat("2005-07-30")]


def filter_rentals(rentals: List[Rental]) -> List[Rental]:
    return [rental for rental in rentals if rental.rental_date <= date.fromisoformat("2005-07-30")]


def process_rental(rental: Rental) -> float:
    # Ausleihgebür
    total_costs: float = 0.0
    rental_end_date: date = min(rental.return_date, date.fromisoformat("2005-07-30"))
    # Rental duration in days. Closed interval (you need to pay for the first day and the last)
    # rental = 5, return = 7 ==> 3 days (7 - 5 + 1)
    rental_duration = (rental_end_date - rental.rental_date).days + 1

    # The days you are over the expected rental duration. First day over it counts:
    # film_rental_duration = 4, rental_duration = 5 ==> 1 (5 - 4)
    days_over = max(0, rental_duration - rental.film_rental_duration)

    # You only need to pay up until 2 * film_rental_duration
    # 9 days over, film_rental_duration = 4 ==> 8
    punished_days_over = min(2 * rental.film_rental_duration, days_over)

    # If you are over 2 times the film_rental_duration, you need to pay the replacement cost
    replacement_cost: float = 0.0
    if days_over > 2 * rental.film_rental_duration:
        replacement_cost = rental.film_replacement_cost

    total_costs += rental.film_rental_rate
    total_costs += punished_days_over
    total_costs += replacement_cost

    print(
        f"Rental {rental.rental_id} from {rental.rental_date} to {rental_end_date}"
        f" spanning {rental_duration} out of {rental.film_rental_duration} days"
    )
    print(f"  It is {days_over} days over and punished for {punished_days_over}.")
    print(f"  It {'must pay' if replacement_cost > 0 else 'must not pay'} the"
          f" replacement cost of {rental.film_replacement_cost}")
    print(
        f"  This sums up to {rental.film_rental_rate:.2f} + {punished_days_over} + {replacement_cost:.2f} = {total_costs:.2f}"
    )

    return total_costs


if __name__ == "__main__":
    total_rental_cost: float = 0.0
    total_payment_given: float = 0.0

    for r in filter_rentals(read_rentals(Path("Rental.tsv"), Path("Film_Infos.tsv"))):
        total_rental_cost += process_rental(r)

    print("")

    for p in filter_payments(read_payments(Path("Payment.tsv"))):
        total_payment_given += p.amount

    print("")
    print(
        f"Total cost: {total_rental_cost:.2f}, Payment: {total_payment_given:.2f},"
        f" Delta: {total_payment_given - total_rental_cost:.2f}"
    )
