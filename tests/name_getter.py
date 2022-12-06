import csv
import json

with open("champions.json") as f:
    data = json.loads(f.read())

name_set = {s["external_name"] for s in data.values() if "external_name" in s}

with open('names.csv', 'w', newline='') as csvfile:
    name_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for this_name in list(sorted(name_set))[1:]:
        name_writer.writerow([this_name])
