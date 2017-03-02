import csv

with open('/home/krish/Shared_Win/Shared/Python/MyCodes/Files/scr1.csv', 'r') as f:
  reader = csv.reader(f)
  list_view = list(reader)

print(list_view "\n")
