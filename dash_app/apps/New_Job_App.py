import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_app.components import dash_reusable_components as drc
from dash.dependencies import Output, Input, Input,State
from dash_app.views.navbar import Navbar
from dash_app.app import app
from utils import default_settings
from dtypes.job import Job
from dtypes.db_helper import Db_helper
import dash
from dtypes.imageData import ImageData
from os import listdir
from skimage import io
import plotly.express as px
import os
from utils.input_utils import *
from dtypes.Spreadsheets import Spreadsheet
from utils.default_settings import *
from dash_app.components.input_col import get_input_col
from dash_app.components.file_col import get_file_col

options = default_settings.get_default_options()
nav = Navbar("Create New Job")
hr = html.Hr(style={'border-top':'3px dashed gray'})
db_helper = Db_helper()
output = html.Div(id = 'output',children = [])

def New_Job():
    layout = html.Div([
            nav,
            output,
            html.Div(id = 'warning', children = []),
            dbc.Row([get_input_col('new',job=True),get_file_col()]),
            html.Div(id = 'view-results'),
            html.Div(id = 'image-prev'),

        ])
    return layout

layout = New_Job()

@app.callback(Output("image-prev",'children'),
        Input('preview-button','n_clicks'),
        State('folder-checks','value'),
        State(component_id='new-thresh', component_property='value'),
        State(component_id='new-warn', component_property='value'),
        State(component_id='new-ignore', component_property='value'),
        State(component_id='new-alt', component_property='checked'),
        State(component_id='new-alt-thresh', component_property='value'),
        State(component_id='new-multi', component_property="checked"),
        State(component_id='new-fiber-type', component_property="value"),
        )
def preview_clicked(n,value,thresh,warn,ignore,alt,alt_thresh,multi,type1):
    if n is None or n==0:
        return dash.no_update
    else:
        print("value in prev :", value)
        image_ls = os.listdir(value[0])
        selected = image_ls[0]
        if selected[0]=='.':
            selected =image_ls[1]
        print("selected ", selected )
        options['constants'] = update_constants(options['constants'],
                                                thresh,
                                                type1,
                                                warn,
                                                ignore,
                                                alt,
                                                alt_thresh,
                                                multi)
        img_path = value[0] + '/' + selected
        img_data = ImageData("preview-job",
                             'preview-frame',
                             img_path,
                             options["constants"],
                             db_helper)
        img_out_path = "./job-data/preview-job/preview-frame" + '/' + selected[:-4] + '_out.png'
        img_np = io.imread(img_out_path)
        fig = px.imshow(img_np,)
        header = html.H3("Threshold Preview")
        graph = dcc.Graph(id = 'img-prev-graph',figure=fig)
        comp_ls = [header,graph]
        return comp_ls


@app.callback(Output(component_id='thresh', component_property='children'),
    [Input(component_id="thresh",component_property='value')]
)
def update_thresh_choice(value):
    options['constants']['thresh'] = float(value)
    return []


@app.callback(Output(component_id='frame_name', component_property='children'),
    [Input(component_id="frame_name",component_property='value')]
)
def update_frame_name_choice(value):
    options['job_name'] = value
    return []

@app.callback(Output(component_id='file-lg', component_property='children'),
              [Input(component_id='upload-image', component_property='contents')],
              [State(component_id='upload-image', component_property='filename'),
               State(component_id='upload-image', component_property='last_modified'),
               State(component_id='file-lg', component_property='children')])
def parse_contents(contents, filename, date, childs):
    print("type of childs : ", type(childs))
    print("type of contents : ", type(contents))
    if contents != None:
        if (type(contents) == type(list())):
            print("list var")

            for content in contents:
                # contents = base64.b64encode(contents)
                print("type of contents:", type(contents))
                s = contents.split(';base64,')[-1]
                options["ref_ls_ls"][0].append(drc.b64_to_numpy(s, False))
                childs.append(dbc.ListGroupItem(id=str(filename), color='primary', children=[
                    html.Div(filename)
                ]))

        else:
            s = contents.split(';base64,')[-1]
            options["ref_ls_ls"][0].append(drc.b64_to_numpy(s, False))
            childs.append(dbc.ListGroupItem(id=str(filename), color='primary', children=[
                html.Div(filename)
            ]))
    if (type(filename) == type(list())):
        for name in filename:
            options['name_ls'].append(name)
    elif filename != None:
        options['name_ls'].append(filename)
    return childs




@app.callback(Output(component_id='program_choice', component_property='children'),
    [Input(component_id='program_choice',component_property='value')]
)
def update_program_choice(value):
    options['program_type'] = value
    return []



@app.callback(Output(component_id='warning', component_property='children'),
              [Input(component_id='new-run', component_property='n_clicks'),
               State(component_id = 'folder-checks',component_property= 'value'),
               State(component_id='new-thresh', component_property='value'),
               State(component_id='new-warn', component_property='value'),
               State(component_id='new-ignore', component_property='value'),
               State(component_id='new-alt', component_property='checked'),
               State(component_id='new-alt-thresh', component_property='value'),
               State(component_id='new-multi', component_property="checked"),
               State(component_id='new-fiber-type', component_property="value"),

              ],
              prevent_initial_call=True
              )

def warns(n_clicks,folders,thresh,warn,ignore,alt,alt_thresh,multi,type):
    if(n_clicks is not None and n_clicks!=0):
        warn_ls = []
        if(options["program_type"] == None):
            warn = dbc.Alert(children=[" \tError: Not all fields completed"], color="danger", dismissable=True)
            warn_ls.append(warn)
        if (len(options["job_name"]) == 0 or options["job_name"] in listdir("./job-data/")):
            warn = dbc.Alert(children=[" \tError: job name already used"], color="danger", dismissable=True)
            warn_ls.append(warn)

        if (len(folders) == 0):
            warn = dbc.Alert(children=[" \tError: No frames selected"], color="danger", dismissable=True)
            warn_ls.append(warn)
        return warn_ls
    else: return []


@app.callback(Output(component_id='view-results', component_property='children'),
              [Input(component_id="new-run", component_property='n_clicks'),
               State(component_id = 'folder-checks',component_property= 'value'),
               State(component_id='new-thresh', component_property='value'),
               State(component_id='new-warn', component_property='value'),
               State(component_id='new-ignore', component_property='value'),
               State(component_id='new-alt', component_property='checked'),
               State(component_id='new-alt-thresh', component_property='value'),
               State(component_id='new-multi', component_property="checked"),
               State(component_id='new-fiber-type', component_property="value"),
               State(component_id='spread', component_property='checked'),
               State(component_id='new-number', component_property="value"),
               ],
              prevent_initial_call=True
              )



def run_button_clicked_new(n,folders,thresh,warn,ignore,alt,alt_thresh,multi,type,sheet,num):

    if n is not None and n!= 0:
        const = get_default_constants()
        const = update_constants(const,thresh,type,warn,ignore,alt,alt_thresh,multi,num)
        options['constants'] = const

    if n is None:
        print("button not clicked ")
        return []

    elif (options["program_type"] != None):
        if(len(folders)!=0):
            for fpath in folders:
                options["frame_paths"].append(fpath)
            print("frame paths in job", options["frame_paths"])
            job = Job(options, db_helper)
            options["frame_paths"]=[]
            #current_job = job
            if sheet:
                for folder in job.frame_ls:
                    Spreadsheet(folder,job.job_name)
            return [dbc.Button("View Results",href="./job_id_" + job.job_id)]
    else:
        return [dbc.Alert(children=[" \tError: Not all fields completed"], color="danger", dismissable=True)]

