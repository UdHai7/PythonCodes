import csv

with open('stg_fct_stock_snapshot.csv', 'rb') as f:

    reader = csv.reader(f)

    for row in reader:

        print row