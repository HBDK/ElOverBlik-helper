from logging import warning, info

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
        info('Creating Database')
        self.Client.create_database(self.Database)

    def GetLatestMeterDate(self, measurementName, friendlyName):
        result = self.Client.query('SELECT last("value"),"Metering date" FROM "' + self.Database + '"."autogen"."'+ measurementName +'" WHERE ("friendly_name" = \'' + friendlyName + '\')')
        try:
            returnString = result.raw['series'][0]['values'][0][-1]
        except:
            warning("no values! is this first time you run this?")
            returnString = ""
        return returnString