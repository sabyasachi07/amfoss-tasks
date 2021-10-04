import sys
import csv
import re

if len(sys.argv) != 3:
    sys.exit("Usage: python dna.py data.csv sequence.txt")
#AGATC,TTTTTTCT,AATG,TCTAG,GATA,TATC,GAAA,TCTG
filedatabase = sys.argv[1]
column = []
names = []
values = []
dna_sequence = []

with open(filedatabase) as csvfile:
    database_reader = csv.reader(csvfile)
    column = next(database_reader)
    for row in database_reader:
        dna_sequence.append(row[1:])
        names.append(row[0])

dna_index = {}
for i in range(len(names)):
    dna_index[names[i]] = dna_sequence[i]

filesequence = sys.argv[2]
sequence_reader = open(filesequence,"r+")
read = sequence_reader.read()

res = []
groups = []
for i in range(len(column)-1):
    groups = max(re.findall(r"(?:{})+".format(column[i+1]), read), key=len)
    res.append(str(len(re.findall(column[i+1], groups))))

for i in range(len(names)-1):
    if set(dna_index[names[i]]) == set(res):
        print(names[i])
        break
    elif i == int(len(names)-2):
        print("No match")