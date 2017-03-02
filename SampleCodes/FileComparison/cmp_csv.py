import csv

def get_key(row):
    return row["!Sample_title"], row["!Sample_geo_accession"]

def load_csv(filename):
    """Put csv data into a dict that maps title/geo to the complete row.
    """
    d = {}
    with open(filename) as f:
        for row in csv.DictReader(f, delimiter=","):
            key = get_key(row)
            assert key not in d
            d[key] = row
    return d

def diffs(old, new):
    yield from added_or_removed("ADDED", new.keys() - old.keys(), new)
    yield from added_or_removed("REMOVED", old.keys() - new.keys(), old)
    yield from changed(old, new)

def compare_row(key, old, new):
    i = -1
    for i, line in enumerate(diffs(old, new)):
        if not i:
            print("/".join(key))
        print("    " + line)
    if i >= 0:
        print()

def added_or_removed(state, keys, d):
    items = sorted((key, d[key]) for key in keys)
    for key, value in items:
        yield "{:10}: {:30} | {:30}".format(state, key, value)

def changed(old, new):
    common_columns = old.keys() & new.keys()
    for column in sorted(common_columns):
        oldvalue = old[column]
        newvalue = new[column]
        if oldvalue != newvalue:
            yield "{:10}: {:30} | {:30} | {:30}".format(
            "CHANGED",
            column, 
            oldvalue.ljust(30),
            newvalue.ljust(30))

    
if __name__ == "__main__":
    oldcsv = load_csv("/home/krish/Shared_Win/Shared/Python/MyCodes/Files/scr1.csv")
    newcsv = load_csv("/home/krish/Shared_Win/Shared/Python/MyCodes/Files/scr1.csv")
    # title/geo pairs that occur in both files:
    common = oldcsv.keys() & newcsv.keys() 
    for key in sorted(common):
        compare_row(key, oldcsv[key], newcsv[key])