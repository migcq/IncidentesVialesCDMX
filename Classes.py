import pandas as pd
from dataclasses import dataclass
from decorators import open_close_connection

@dataclass
class Datos():

    path:str

    def read_data(self,sep=","):
        data = pd.read_csv(self.path, sep=sep)
        
        return data
    
    def unique_values(self,data,column):
        values = data[column].unique()
        
        return values


@dataclass
class ClaseMongo():

    JSON:str
    db_name:str
    column_name: str
    
    @open_close_connection
    def find(self,conn):
        response = list(connection[self.db_name][self.column_name].find(self.JSON))
        
        response = pd.DataFrame(response)
        
        return response
        
    @open_close_connection
    def insert(self,conn=None):
        conn[self.db_name][self.column_name].insert(self.JSON)
    
    @open_close_connection
    def update(self,JSET, conn=None):
        connection[self.db_name][self.column_name].update(self.JSON,{"$set":JSET})
