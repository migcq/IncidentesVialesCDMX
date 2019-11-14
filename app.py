import os
import dash 

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.exceptions import PreventUpdate

from pymongo import MongoClient

from dash.dependencies import Input, Output

from sistema import Directorio
from Classes import Datos, ClaseMongo

directorio = "./Datos"
objDirectorio = Directorio(directorio)
lista_archivos = objDirectorio.read_file_names()
options = [{"label":label,"value":label} for label in lista_archivos]


app = dash.Dash (__name__ , external_stylesheets=[dbc.themes.BOOTSTRAP])
Elem_1 = html.Div([html.H1("Controles", className = "display-1"), 
        dcc.Input(id="test_input",className ="alert alert-secondary"), 
        dcc.Dropdown(id="lista_archivos", options = options)])
Elem_2 = html.Div([html.H2("Respuestas", id="respuesta", className = "display-4"),html.Div(id="div-respuesta")])

Elem_3 = html.Div([])

app.layout = html.Div ([Elem_1,Elem_2,dcc.Dropdown(id="column",options=[])], className ="alert alert-primary")


@app.callback (Output("respuesta","children"), [Input("test_input","value")])
def test_callback (valor):  # valor hace referencia al "value" de Input
    return valor


@app.callback (Output("column","options"), [Input("lista_archivos","value")])
def regresa_columnas (nombre_archivo):  #nombre_archivo hace referencia al "value" del Input
    if not nombre_archivo == None:
        path = f"./datos/{nombre_archivo}"
        objDatos = Datos(path)
        if nombre_archivo=="incidentes-viales-c5.csv":
            comma=";"
        else: comma=","
        df = objDatos.read_data(comma)
        options = [{"label":label,"value":label} for label in df.columns]
    else: options = []
    return options

@app.callback (Output("div-respuesta","children"), [Input("column","value"),Input("lista_archivos","value")])
def cargar_respuesta (columna,nombre_archivo):
    if not nombre_archivo == None:
        path = f"./datos/{nombre_archivo}"
        objDatos = Datos(path)
        if nombre_archivo=="incidentes-viales-c5.csv":
            comma=";"
        else: comma=","
        df = objDatos.read_data(comma)
        v_unicos = objDatos.unique_values(df,columna)
        print("Valores unicos: ", v_unicos)
        JSON = {str(index):value for index,value in enumerate(v_unicos)}
        print("Cadena JSON: ", JSON)
        objMongo = ClaseMongo(JSON,"db_prueba","collection")
        objMongo.insert()

        resultado = "Datos guardados"
    else: resultado = ""
    return resultado

if __name__ == '__main__':
    app.run_server(debug=True)
