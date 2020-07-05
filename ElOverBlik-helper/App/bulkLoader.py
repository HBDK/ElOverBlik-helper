from Einfluxer import Einfluxer

from csv import reader
from influxdb import InfluxDBClient
from os import environ
from json import load as loadJson
import logging
from pytz import timezone
from datetime import datetime, timedelta

options = {}
optionsFile = '/data/options.json'

TOKENKEY = "token"

try:
    options[TOKENKEY] = environ['SUPERVISOR_TOKEN']
    options['baseUrl'] = 'http://supervisor/core/api/states/'
except:
    logging.warning("Couldn't get token from Enviroment assuming this is dev")
    optionsFile = 'local.json'

with open(optionsFile) as json_file:
    options.update(loadJson(json_file))

localtimezone = timezone(options["Timezone"])
measurementName = options["db_measurement_name"]
headers = []

def get_time(input):
    return datetime.strptime(input, "%Y-%m-%d %H.%M").astimezone(localtimezone) + timedelta(minutes=59 ,seconds=59)

def createPoint(row):
    tags = {}
    tags['ingest time'] = datetime.now().astimezone(localtimezone)
    
    for i in range(1,len(row)):
        if headers != '':
            tags[headers[i]] = row[i]

    if tags["Måleenhed"] == "KWH":
        tags["unit_of_measurement"] = "kWh"
    else:    
        tags["unit_of_measurement"] = tags["Måleenhed"]
    tags["Metering date"] = tags["Fra dato"].split(" ")[0]

    return {    "measurement": measurementName,
                "time": get_time(tags["Fra dato"]),
                "tags": tags,
                "fields": {
                    "value": float(tags['Mængde'].replace(",","."))
            }}

with open("Meterdata.csv") as csvfile:
    data = list(reader(csvfile, delimiter=';'))
    headers = data[0]
    result = []
    for row in data[1:]:
        test = createPoint(row)
        result.append(test)

client = InfluxDBClient(host=options['db_ip'], port=options['db_port'], username=options['db_user'], password=options['db_pass'])
Einf = Einfluxer(client, options['db_name'])
Einf.Client.write_points(result)