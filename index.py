#import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH
from numpy import ndarray
#import dash_bootstrap_components as dbc
#import dash_app.components.dash_reusable_components as drc
import sqlite3
from utils.sql_utils import convert_array,adapt_array
import os
from dash_app.app import app
#from dash_app.views.navbar import Navbar
#from dash_app.views.view_job import View_Job
#from dash_app.views.view_frame import View_Frame
#from dash_app.views.homepage import Homepage
#from dash_app.views.new_job import new_job_page
from dash_app.apps import New_Job_App
from dash_app.apps import homepage
from dash_app.apps import View_Job_App
from dash_app.apps import View_Prev_Jobs
from tkinter import Tk
from tkinter.filedialog import askdirectory
import dash
import threading




app.layout = html.Div([
    dcc.Location(id = 'url', refresh= False),
    html.Div(id = 'page-content')
])
server = app.server

@app.callback(Output('page-content','children'), 
            [Input('url', 'pathname')])
def display_page(pathname):
    print("gonna make new layout")
    if pathname == "/prev-jobs":
         return View_Prev_Jobs.layout()
    if pathname == "/new-job":

        return New_Job_App.New_Job()
    if pathname == "/edit-job":
        return '404'
    if '/job_id_' in pathname:
        print("returning view Job")
        return View_Job_App.layout
    else:
        print("starting homepage")
        return homepage.layout



"""

@app.callback(
    Output({'type': 'dynamic-out', 'index': MATCH}, 'children'),
    Input({'type': 'list-button', 'index': MATCH,}, 'n_clicks'),
    State({'type': 'list-button', 'index': MATCH}, 'children'),
)
def add_out(n_clicks,child):
    print("this is id",child)
    print("is this it :",child[0]["props"]["id"])
    print(type(child))
    print("so at least it was called tho ")
    if(n_clicks== 0):
        return []
    else:
        #return [View_Frame(child[0]["props"]["id"])]
        return []


@app.callback(
    Output(component_id='img-sec', component_property = 'children'),
    Input({'type': 'list-button'}, 'n_clicks')
)
def add_out(n_clicks,):
    if(n_clicks== 0):
        return []
    else:
        return [html.Div("Test")]

STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')


@app.server.route('/static/<resource>')
def serve_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)
"""


if __name__ == '__main__':
    app.run_server(debug = True)



