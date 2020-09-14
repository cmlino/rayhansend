import requests
import re
import csv
import datetime 
url = "https://portal.rockgympro.com/portal/public/5b68a6f4de953dcb1285dc466295eb59/occupancy"

response = requests.request("GET", url)

# print(response.text.encode('utf8'))
# extract count using regex
people = str((re.search(r"'count' : (\d+)", response.text).group(1)))
time = str((datetime.datetime.now()))

fields = [people, time]
with open('edge_data.csv', 'a') as csvfile:
    writer = csv.writer(csvfile) 
    writer.writerow(fields)