from logging import warning, info

class Einfluxer:

    def __init__(self, client, database, retentionPolicy):
        self.Client = client
        self.Database = database
        self.retentionPolicy = retentionPolicy

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
    
    def GotValuesForDate(self, data, measurementName, name):
        query = 'SELECT last("value") FROM "' + self.Database + '"."' + self.retentionPolicy + '"."'+ measurementName +'" WHERE ("metering_date" = \'' + data["tags"]["metering_date"] + '\' AND ("Name" = \'' + name + '\' OR "Name" = \'\')) GROUP BY "Name"'
        result = self.Client.query(query)
        return len(result.raw['series']) > 0
