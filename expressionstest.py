import re

f = open("datamail.txt")

lines = f.read()
# let us read each line separately
linebreaks = lines.split("\n")

f.close()
result = []
for stop in linebreaks:
    pattern = re.search("@", stop)
    if pattern != None:
        print(stop)


#print(result)