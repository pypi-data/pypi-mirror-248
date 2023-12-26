from urllib.request import urlretrieve
import os
import csv

if not os.path.exists("enginehash.csv"):
    urlretrieve("https://raw.githubusercontent.com/Impact-I/reFlutter/main/enginehash.csv", "enginehash.csv")

with open("enginehash.csv") as f_obj:
    read = csv.DictReader(f_obj, delimiter=',')
    row_count = sum(1 for _ in read)
    f_obj.seek(0)
    reader = csv.DictReader(f_obj, delimiter=',')
    i = -row_count
    for line in reader:
        i = i + 1
        print(i, line['Snapshot_Hash'], line['Engine_commit'])