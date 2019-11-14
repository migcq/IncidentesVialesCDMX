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

    def get_values(self,dataframe, column):
        valid_columns = ['dia_semana', 'mes_cierre', 'delegacion_inicio']
        if column in valid_columns:
            agg_values = dataframe.groupby(column).agg({'folio':'count'})
            values = agg_values.to_dict()

        else: 
            values = []
        return values



@dataclass
class ClaseMongo():

    JSON:str
    db_name:str
    column_name: str
    
    @open_close_connection
    def find(self,conn=None): #Para definir/saber que es un valor que se espera, pero que en esta funcion no se define
        response = list(conn[self.db_name][self.column_name].find(self.JSON))
        
        response = pd.DataFrame(response)
        
        return response
        
    @open_close_connection
    def insert(self,conn=None):
        conn[self.db_name][self.column_name].insert(self.JSON)
    
    @open_close_connection
    def update(self,JSET, conn=None):
        conn[self.db_name][self.column_name].update(self.JSON,{"$set":JSET})
