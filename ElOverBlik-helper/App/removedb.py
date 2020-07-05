from Einfluxer import Einfluxer

from influxdb import InfluxDBClient
from os import environ
from json import load as loadJson
import logging

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

client = InfluxDBClient(host=options['db_ip'], port=options['db_port'], username=options['db_user'], password=options['db_pass'])
Einf = Einfluxer(client, options['db_name'])
logging.warning("Removing DB")
Einf.Client.drop_database(options['db_name'])
