import pandas as pd
import pickle
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, Input
from dash_app.views.navbar import Navbar

#create top bar for navigation
nav = Navbar()
#create buffer to add space before header
buffer = html.Hr(style={"border": "15px"})
#create header
header = html.H3("Create New Job", style={"text-align": "center"})
#add separator after header
hr = html.Hr(style={"border": "6px solid light grey"})
#sub
output = html.Div(id = 'output',children = [])

#creates selelector for program choice 
program_choice = dbc.Select(id = "program_choice", 
    options=[
        {"label": "Light Fibers", "value": "1"},
        {"label": "Dark Fibers", "value": "2"},
        {"label": "Circle Detection", "value": "3"}
    ]
)


#creates image selector
img_selector = dcc.Upload(
    id="upload-image",
    children=[
        "Drag and Drop or ",
        html.A( id='upload-label',children="Select an Image"),
    ],
    # No CSS alternative here
    style={
        "color": "darkgray",
        "width": "100%",
        "height": "50px",
        "lineHeight": "50px",
        "borderWidth": "1px",
        "borderStyle": "dashed",
        "borderRadius": "5px",
        "borderColor": "darkgray",
        "textAlign": "center",
        "padding": "2rem 0",
        "margin-bottom": "2rem",
    },
    #accept="*",
    )
folder_selector = dbc.ListGroup([

])


#create file list group
file_lg = dbc.ListGroup(id="file-lg",children=
    [
        dbc.ListGroupItem("test", color = "primary")
    ]

)

thresh = html.Div(id = "adjust-threshold",children=[
    html.H6("Adjust Threshold"),
    dbc.Input(id ="thresh", placeholder="default is 73", type = "text", value = '73'),
])

warn = html.Div(id ="alert-on",children=[
    html.H6("Size to Alert On"),
    dbc.Input(id ="warn", placeholder="default is 5000", type = "text", value = '5000'),
])


ignore = html.Div(id = "ignore",children=[
    html.H6("Size to ignore"),
    dbc.Input(id ="ignore", placeholder="default is 20", type = "text", value = '20'),
])

"""run_card = dbc.Card(color=" secondary", inverse=True,children=[
    dbc.CardBody([
        html.H4("Confirm Details"),
        dbc.Button("Run Job", id= "run-button1", color = "primary")
    ])
    ],
       style = {"width":"18rem"}
)
"""
input_choice = dbc.Select(id = "input_choice", 
    options=[
        {"label": "Images that create frame", "value": "1"},
        {"label": "Frames(folder(s) of images)", "value": "2"},
        {"label": "Each image is Frame", "value": "3",}
    ]
)

job_details_card = dbc.Card(color = "info", children = [
    html.H4("Job Details"),
    html.Div("select program to run"),
    program_choice,
    html.Div("Job name"),
    dbc.Input("frame_name", placeholder="Enter a name for this Job",type="text"),
])

main =  html.Div(id = 'main',
    children = [
        dbc.Row(
            dbc.Col(
                header,
                width={"size": 6, "offset": 3},
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    #html.Div("The first of three columns"),
                    children=[
                        job_details_card,
                        hr,
                        html.Br(),
                        html.H4("Input details"),
                        html.Div("Select input type"),
                        input_choice,
                        html.Br(),
                        thresh,
                        html.Br(),
                        warn,
                        html.Br(),
                        ignore,
                        #html.Div("Adjust threshold"),
                        #dbc.Input(id ="thresh", placeholder="default is 73", type = "text", value = '73'),
                        html.Br(),

                        ], 
                        style={"text-align": "left"},
                    
                    width={"size": 3, "order": 1, "offset": 1},
                ),
                dbc.Col(
                    #html.Div("Job name"),
                    children=[
                        html.H4("Select Files"),
                        img_selector,
                        hr,
                        html.Div("Selected files/frames:"),
                        file_lg,
                    ],
                    width={"size": 6, "order": 12,"offset":1},
                ),
            ]
        ),
        dbc.Row(
            [#html.Button("run job", id='button'),
                dbc.Col(
                    children =[
                        #run_card,
                        
                        dbc.Button("Run Job", id= "run-button", color = "primary", disabled = False)
                    ],
                    width={"size": 9, "order": 12,"offset":1},
                )
        ]
            


        )
        
        
    ]
)




def new_job_page():
    layout = html.Div([
        nav,
        buffer,
        output,
        html.Div(id = "warning", children =[]),
        main,
    ])
    return layout

app = dash.Dash(__name__, external_stylesheets=dbc.themes.DARKLY)


