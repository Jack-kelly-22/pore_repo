import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH
import sqlite3
from utils.sql_utils import get_job_fetch_str
from dtypes.db_helper import Db_helper
from dash_app.views.navbar import Navbar
from dash_app.app import app
db_helper = Db_helper()
fetch_str = get_job_fetch_str()
#dcc.Location(id = 'url2', refresh= False),
buffer = html.Hr(style={"border": "15px"}),
# create header
header1 = html.H3("Previous Jobs", style={"text-align": "center"})
# add separator after header
hr = html.Hr(style={"border": "6px solid light grey"})
nav = Navbar("View Previous Jobs")

def refresh_jobs():
    job_ls = db_helper.fetch_jobs()
    list_item_ls = []
    i=0
    for job in job_ls:
        item = dbc.ListGroupItem([
            dbc.Col(
                dbc.ListGroupItemHeading(str(job["job_name"])),
            ),

            dbc.Col(
                dbc.Button("view",
                   style={"float": "right"},
                   key=job["job_id"],
                   href="/job_id_" +job["job_id"])
            ),
            dbc.Row([
                #dbc.Col(dbc.ListGroupItemText("Date:", job["job_date"]), width=2),
                #dbc.Col(dbc/)
                dbc.Col(dbc.ListGroupItemText("# of Frames:" + str(len(job["frame_data_ls"]))), width=2),
            ])
        ])
        i=i+1


        list_item_ls.append(item)
        list_item_ls.reverse()
    return list_item_ls


def layout():
    job_list = dbc.ListGroup(children=refresh_jobs())

    layout = html.Div([
        nav,
        dbc.Container([

            header1,
            job_list
        ])
    ])
    return layout




@app.callback(Output('url2','pathname'),
    Input(component_id='view-button', component_property='n_clicks'),
    Input(component_id='view-button', component_property='key'),
)
def view_button_clicked(n_clicks,key):
    if(n_clicks == 0):
        return
    else:
        return "/view-job_" + key





