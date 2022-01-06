from Extractor import Extractor, ExtractorBuilder
from Einfluxer import Einfluxer

from influxdb import InfluxDBClient
from datetime import datetime
from requests import post
from os import environ
from json import load as loadJson
from sys import exc_info
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
extractors = ExtractorBuilder(options).build()
Einf = Einfluxer(client, options['db_name'], options['db_retention_policy'])

cumulativeMessage = ""

for extractor in extractors:

    message = ""

    try:
        data = extractor.GetMeasurements()
    except ValueError:
        message = "Got ValueError when fetching data from Home assistant, The sensor probably haven't fetched data yet."

    if message == "":
        
        if not Einf.GotValuesForDate(data[0],extractor.measurementName,extractor.name):
            message = "Inserted data for: {}".format(data[0]['tags']['Metering date'])
            try:
                Einf.Client.write_points(data)
            except:
                e = exc_info()[0]
                message = "Inserted data for: {}".format(data[0]['tags']['Metering date'])
                message += "\nBut got:\n {}".format(e)
                logging.error(e.with_traceback)
        else:
            message = "Ran but already had data for: {}".format(data[0]['tags']['Metering date'])

    logging.info(message)
    cumulativeMessage += message

if "webhookUrl" in options.keys() and not options["webhookUrl"] == "":
    result["message"] = cumulativeMessage
    result["time"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    result["options"] = options
    result["options"][TOKENKEY] = ""
    if optionsFile != 'local.json':
        try:
            post(options["webhookUrl"], json=result)
        except:
            logging.error("Could not post to: {}".format(options["webhookUrl"]))
    else:
        logging.warning("skipping webhook post")
