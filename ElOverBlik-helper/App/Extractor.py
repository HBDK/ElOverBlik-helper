from requests import get
from datetime import datetime
from logging import warning
from pytz import timezone

class Extractor:
    def __init__(self, baseUrl, sensorPrefix, token, localTimezone, measurementName, name):
        self.baseUrl = baseUrl
        self.sensorPrefix = sensorPrefix
        self.header = {
                    "Authorization": "Bearer " + token,
                    "content-type": "application/json",
                }
        self.localtimezone = timezone(localTimezone)
        self.measurementName = measurementName
        self.name = name

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

        data['attributes']['ingest time'] = datetime.now().astimezone(self.localtimezone)
        time = self.GetTime(data['attributes']['Metering date'],hour)

        isoCalendar = time.isocalendar()

        data['attributes']['Week Number'] = isoCalendar[1]
        data['attributes']['Year'] = isoCalendar[0]
        data['attributes']['day of week'] = isoCalendar[2]
        data['attributes']['Week and year'] = str(isoCalendar[0]) + "-" + str(isoCalendar[1])
        data['attributes']['Month and year'] = str(time.month) + "-" + str(time.year)
        data['attributes']['Name'] = self.name

        return {    "measurement": self.measurementName,
                    "time": time,
                    "tags": data['attributes'],
                    "fields": {
                        "value": float(data['state'])
                    }}

    def GetTime(self, date, hour):
        date = date.split('-')
        return datetime(int(date[0]), int(date[1]), int(date[2]), hour, 59, 59).astimezone(self.localtimezone)

    def GetMeasurements (self):
        data = []

        for i in range(24):
            data.append(self.CreateMeasurement(i))

        return data

class ExtractorBuilder:
    def __init__(self, options):
        self.token = options["token"]
        self.options = options

    def build(self):
        Extractors = []

        if "sets" in self.options and len(self.options["sets"]):
            for options in self.options["sets"]:
                Extractors.append(Extractor(self.options['baseUrl'],options['sensorPrefix'],self.token, self.options['Timezone'],self.options['db_measurement_name'], options["name"]))

        else:
            Extractors.append(Extractor(self.options['baseUrl'],self.options['sensorPrefix'],self.token, self.options['Timezone'],self.options['db_measurement_name'],self.options['db_measurement_name']))
        
        return Extractors