## About

This is a python implementation of Exercise 11 and therefore can not be easily
translated to a SQL-Query. That's why I feel I can release the source code
here, it is meant to work out the god damn assignment task, as apparently
everything is wrong.

## How to use this

1. Check if your id is 276.
2. If not, run all the `*.sql` statements with your ID and copy the WHOLE
   RESULTSET, inlcuding the header in the corresponding `.tsv` file.
3. Run `python solver.py`
4. Run the query `SELECT <your id>, <the delta> FROM rental WHERE ROWNUM <= 1` to only output that result
