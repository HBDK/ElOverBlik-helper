from Extractor import Extractor
from Einfluxer import Einfluxer

from influxdb import InfluxDBClient
from datetime import datetime
from requests import post
from os import environ, path
from json import load as loadJson
import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

options = {}
optionsFile = '/data/options.json'

try:
    options['token'] = environ['SUPERVISOR_TOKEN']
    options['baseUrl'] = 'http://supervisor/core/api/states/'
except:
    optionsFile = 'local.json'

with open(optionsFile) as json_file:
    options.update(loadJson(json_file))

logging.info(options['db_name'])
logging.info(datetime.now())

client = InfluxDBClient(host=options['db_ip'], port=options['db_port'])
extractor = Extractor(options['baseUrl'],options['sensorPrefix'],options['token'])
Einf = Einfluxer(client, options['db_name'])

data = extractor.GetMeasurements()

if not data[0]['tags']['Metering date'] == Einf.GetLatestMeterDate():
    logging.info("Inserting data for " + data[0]['tags']['Metering date'])
    Einf.Client.write_points(data)
else:
    logging.info("Noope we GOood")

#Einf.Client.drop_database(options['db_name'])