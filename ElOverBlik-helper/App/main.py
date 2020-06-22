from influxdb import InfluxDBClient
from datetime import datetime
from requests import get, post
from os import environ, path
from json import load as loadJson

options = {}
optionsFile = '/data/options.json'

try:
    options['token'] = environ['SUPERVISOR_TOKEN']
    options['baseUrl'] = 'http://supervisor/core/api/states/'
except:
    optionsFile = 'local.json'

with open(optionsFile) as json_file:
    options.update(loadJson(json_file))

print(options['db_name'])
print(datetime.now())

class Einfluxer:

    def __init__(self, client, database):
        self.Client = client
        self.Database = database

        if not self.DbExsist(self.Database):
            self.CreateDb()
        
        self.Client.switch_database(self.Database)

    def DbExsist(self, name):
        for db in self.Client.get_list_database():
            if db['name'] == name:
                return True
        return False
    
    def CreateDb(self):
        print('Creating Database')
        self.Client.create_database(self.Database)

    def GetLatestMeterDate(self):
        result = self.Client.query('SELECT last("value"),"Metering date" FROM "' + self.Database + '"."autogen"."Energy"')
        try:
            returnString = result.raw['series'][0]['values'][0][-1]
        except:
            print("no values! is this first time you run this?")
            returnString = ""
        return returnString
    
class Extractor:
    def __init__(self, baseUrl, sensorPrefix, token):
        self.baseUrl = baseUrl
        self.sensorPrefix = sensorPrefix
        self.header = {
                    "Authorization": "Bearer " + token,
                    "content-type": "application/json",
                }

    def GetResponse(self, sensorPostfix):
        url = self.baseUrl + self.sensorPrefix + sensorPostfix
        return get(url, headers=self.header)

    def CreateMeasurement(self, hour):
        response = self.GetResponse(str(hour)+"_"+str(hour+1))
        if not response.status_code == 200:
            print(response.url + " " + str(response.status_code))
        data = response.json()
        data['attributes']['ingest time'] = datetime.now().timestamp()

        return {    "measurement": "Energy",
                    "time": self.GetTime(data['attributes']['Metering date'],hour),
                    "tags": data['attributes'],
                    "fields": {
                        "value": data['state']
                    }}

    def GetTime(self, date, hour):
        date = date.split('-')
        return datetime(int(date[0]), int(date[1]), int(date[2]), hour, 30)

    def GetMeasurements (self):
        data = []

        for i in range(24):
            data.append(self.CreateMeasurement(i))

        return data

client = InfluxDBClient(host=options['db_ip'], port=options['db_port'])
extractor = Extractor(options['baseUrl'],options['sensorPrefix'],options['token'])
Einf = Einfluxer(client, options['db_name'])

data = extractor.GetMeasurements()

if not data[0]['tags']['Metering date'] == Einf.GetLatestMeterDate():
    print("Inserting data for " + data[0]['tags']['Metering date'])
    Einf.Client.write_points(data)
else:
    print("Noope we GOood")

#Einf.Client.drop_database(options['db_name'])