import csv

total = 0

with open("data.csv", "r")  as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        for row in line:
            total += int(row)

    csv_file.close()

with open('result.txt', 'w') as f:
    f.write(f"The total is: {total}")