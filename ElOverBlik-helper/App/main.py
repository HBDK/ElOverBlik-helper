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

client = InfluxDBClient(host=options['db_ip'], port=options['db_port'], username=options['db_user'], password=options['db_pass'])
extractor = Extractor(options['baseUrl'],options['sensorPrefix'],options[TOKENKEY], options['Timezone'])
Einf = Einfluxer(client, options['db_name'])

message = ""

try:
    data = extractor.GetMeasurements()
except ValueError:
    message = "Got ValueError when fetching data from Home assistant, The sensor probably haven't fetched data yet."

if message == "":
    if not data[0]['tags']['Metering date'] == Einf.GetLatestMeterDate():
        message = "Inserted data for: {}".format(data[0]['tags']['Metering date'])
        Einf.Client.write_points(data)
    else:
        message = "Ran but already had data for: {}".format(data[0]['tags']['Metering date'])

logging.info(message)

if "webhookUrl" in options.keys() and not options["webhookUrl"] == "":
    result["message"] = message
    result["time"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    result["options"] = options
    result["options"][TOKENKEY] = ""
    try:
        post(options["webhookUrl"], json=result)
    except:
        logging.error("Could not post to: {}".format(options["webhookUrl"]))
    

if optionsFile == 'local.json':
    logging.warning("Removing database")
    #Einf.Client.drop_database(options['db_name'])