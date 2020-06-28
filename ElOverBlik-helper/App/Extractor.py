from requests import get
from datetime import datetime
from logging import warning

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
            warning("Got status {} from {}".format(response.status_code,response.url))
        data = response.json()

        if data['state'] == 'unknown':
            raise ValueError('Value for ' + data['entity_id'] + ' was Unknown')

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