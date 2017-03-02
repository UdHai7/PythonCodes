
data1 = {}
with open("file1.csv", "rb") as in_file1:
     reader1 = csv.reader(in_file1)
     for row1 in reader1:
         data1[row1[0]] = row1[1]
with open("file2.csv","rb") as in_file2, open("file3.csv","wb") as out_file:
    reader2 = csv.reader(in_file2)
    writer = csv.writer(out_file)
    for row2 in reader2:
        if row2[0] in data1:
            row2.append(data1[row2[0]])
        writer.writerow(row2)