-- Values calculated in python to test whether my interpretation is correct
-- THIS IS NOT A SUBMISSION
SELECT R.INVENTORY_ID, RENTAL_DURATION, RENTAL_RATE, REPLACEMENT_COST FROM rental R
LEFT JOIN inventory I
  ON I.inventory_id = R.inventory_id
LEFT JOIN film F
  ON F.film_id = I.film_id
WHERE R.customer_id = 276
ORDER BY R.inventory_id DESC
