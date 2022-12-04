import requests
import json
import csv
import pandas as pd

response_API = requests.get(
    "https://datausa.io/api/data?drilldowns=Nation&measures=Population"
)

data = response_API.text
parse_json = json.loads(data)
print(parse_json["data"])

data_file = open("data_file.csv", "w")
csv_writer = csv.writer(data_file)
count = 0
for emp in parse_json["data"]:
    if count == 0:  # Writing headers of CSV file
        header = emp.keys()
        csv_writer.writerow(header)
        count += 1  # Writing data of CSV file
    csv_writer.writerow(emp.values())

data_file.close()
