from Extractor import Extractor
from Einfluxer import Einfluxer

from influxdb import InfluxDBClient
from datetime import datetime
from requests import post
from os import environ, path
from json import load as loadJson
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO)

logging.info("Starting El overblik helper")

result = {}
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

logging.info("Got {} for database".format(options['db_name']))

client = InfluxDBClient(host=options['db_ip'], port=options['db_port'])
extractor = Extractor(options['baseUrl'],options['sensorPrefix'],options[TOKENKEY])
Einf = Einfluxer(client, options['db_name'])

data = extractor.GetMeasurements()

message = ""

if not data[0]['tags']['Metering date'] == Einf.GetLatestMeterDate():
    messeage = "Inserted data for: {}".format(data[0]['tags']['Metering date'])
    Einf.Client.write_points(data)
else:
    messeage = "Ran but already had data for: {}".format(data[0]['tags']['Metering date'])

logging.info(messeage)

if "webhookUrl" in options.keys() and not options["webhookUrl"] == "":
    result["messeage"] = messeage
    result["time"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    result["options"] = options
    result["options"][TOKENKEY] = ""
    try:
        post(options["webhookUrl"], json=result)
    except:
        logging.error("Could not post to: {}".format(options["webhookUrl"]))
    

#Einf.Client.drop_database(options['db_name'])