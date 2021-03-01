import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash
from dash_app.components.input_col import get_input_col
from numpy import array
from dash_bootstrap_components import Table
from dash_app.liveImage import LiveImage
from dtypes.imageData import ImageData
from dash.dependencies import Output,Input,State
from dash_app.app import app
from dash_app.components import dash_reusable_components as drc
from dash_app.views.navbar import Navbar
import plotly.express as px
from utils.default_settings import get_default_constants
from dash_app.components.live_comps import *
nav = Navbar("Dashboard")
hr = html.Hr(style={'border-top':'3px dashed gray'})
header = html.H2("Live Thresholding")


run_button = dbc.Button("Run Sample",id = 'live-run')


# creates image selector

img_selector = dcc.Upload(
    id="live-upload",
    children=[
        "Drag and Drop or ",
        html.A(id='upload-label', children="Select an Image"),
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

)
img_view_og = html.Div(id = "og-img")
img_view_live = html.Div(id="live-img")
img_store = dcc.Store(id = 'file-store')
img_col = dbc.Col([html.H3("Import a Picture"),img_selector,img_view_og,img_store])

def Homepage():
    layout = html.Div([
        nav,
        dbc.Row([get_input_col('home'),img_col]),
        dbc.Row([img_view_live])
    ])
    return layout

layout = Homepage()

@app.callback(Output(component_id='file-store', component_property='data'),
              [Input(component_id='live-upload', component_property='contents')],
              [State(component_id='live-upload', component_property='filename'),
               ])
def parse_contents(contents, filename):

    if contents != None:
        print("call back trig")
        if (type(contents) == type(list())):
            print("was list")
            return ["d"]

        else:
            s = contents.split(';base64,')[-1]
            img = (drc.b64_to_numpy(s, False))
            js = {'img':s}
            print("just stored image ")
            return js

@app.callback(Output(component_id= 'og-img',component_property='children'),
              [Input(component_id='file-store',component_property='data')])
def show_original_image(data):
        if data != None:
            print("type:", type(data['img']))
            img = (drc.b64_to_numpy(data['img'], False))
            fig = px.imshow(img)
            # Shape defined programatically
            fig.update_layout(dragmode="drawcircle",
                              autosize=False,
                              margin=dict(l=0, r=0, b=0, t=10, pad=2),
                              )
            config = {
                "modeBarButtonsToAdd": [
                    "drawline",
                    "drawclosedpath",
                    "drawcircle",
                    "eraseshape",
                ]
            }

            og_img = dcc.Graph(id="og-graph", figure=fig, config=config)
            return [html.H3("Original image:"),og_img]

@app.callback(Output(component_id="live-img",component_property='children'),
              Input(component_id='home-run', component_property='n_clicks'),
              State(component_id='home-thresh',component_property='value'),
              State(component_id='home-warn',component_property='value'),
              State(component_id='home-ignore', component_property='value'),
              State(component_id='home-alt', component_property='checked'),
              State(component_id='home-alt-thresh', component_property='value'),
              State(component_id='home-multi', component_property="checked"),
              State(component_id='home-fiber-type', component_property="value"),
              State(component_id='file-store', component_property='data'),
              State(component_id='home-number', component_property='value'),

              )
def update_live(n_clicks, thresh_v,warn_v,ignore_v,alt_v,alt_thresh_v,mult,fiber,data,num):
    if n_clicks is not None and n_clicks != 0:
        print("n_clicks: ", n_clicks)
        print("live_thresh :", thresh_v)
        print('warn on', warn_v)
        print('ignore', ignore_v)
        print("alt_v:", alt_v, type(alt_v))
        const = get_default_constants()
        const['thresh'] = int(thresh_v)
        const['fiber_type'] = fiber
        const['warn_size'] = int(warn_v)
        const['min_ignore'] = int( ignore_v)
        const['use_alt'] = bool(alt_v)
        const['alt_thresh'] = int(alt_thresh_v)
        const['multi'] = bool(mult)
        const['num_circles'] = int(num)
        img_data = ImageData("preview-job","preview-frame",'',const,None,dat=data['img'])
        #live_img = LiveImage(data['img'],const)
        fig = px.imshow(img_data.out_image)
        # Shape defined programatically
        fig.update_layout(dragmode="zoom",
                          autosize=False,
                          margin=dict(l=0, r=0, b=0, t=10, pad=2),
                          )
        config = {
            "modeBarButtonsToAdd": [
                "drawline",
                "drawclosedpath",
                "drawcircle",
                "eraseshape",
            ]
        }
        if const['use_alt']:
            th = const['alt_thresh']
        else:
            th = const['thresh']
        summary_table = create_summary_table(img_data.porosity,
                                             img_data.largest_areas[0],
                                             img_data.largest_holes[0],
                                             const["warn_size"],
                                             th,
                                             float(const['scale'])
                                             )
        hole_table = create_hole_table(img_data.largest_holes,const['scale'])
        pore_table = create_pore_table(img_data.largest_areas,const['scale'])
        new_img = dcc.Graph(id="new-graph", figure=fig, config=config)
        image_col =dbc.Col([html.H3("Out image:"), summary_table, new_img],width={'offset':1,'width':'7'})
        table_col = dbc.Col([hole_table,pore_table])
        return dbc.Row([image_col,table_col])
    else:
        return dash.no_update

