import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash_app.app import app
from dash_app.views.navbar import Navbar
import dash_bootstrap_components as dbc
from dtypes.db_helper import Db_helper
from dash_app.components.table_comps import *
from utils.graph_utils import *
import dash_table as dt
import plotly.express as px
import flask
import os
from pandas import DataFrame
from dash_app.components.live_comps import *
from dash_app.components.hist_comp import *
import re
import base64
from skimage import io



def get_view_frame_button(frame_id,i):
    view_button = dbc.Button("See Details",
                             id={'type': "view_frame_button", 'index': i},
                             color="info",
                             key= frame_id)
    return view_button



def update_view_image(path):
    graph_config = {
        "modeBarButtonsToAdd": [
            "drawline",
            "drawclosedpath",
            "drawcircle",
            "eraseshape",
        ]
    }
    img_np_out = io.imread(path)
    img_np_in = io.imread(path[:-6] +'g.png')

    heat_ls = []
    if(os.path.isfile(path[:-8] + "_pore_heatmap.png")):
        heat_img = io.imread(path[:-8] + "_pore_heatmap.png")
        heat_ls.append(heat_img)
    if (os.path.isfile(path[:-8] + "_pore_diff_heatmap.png")):
        heat_diff = io.imread(path[:-8] + "_pore_diff_heatmap.png")
        heat_ls.append(heat_diff)
    heat_row_child =[]

    for heat in heat_ls:
        fig = px.imshow(heat,template="plotly_dark")
        fig.update_layout(dragmode="zoom",
           autosize=False,
           margin=dict(l=0, r=0, b=0, t=10, pad=2),
           width=450,
           height=300
        )
        graph = dcc.Graph(id="heat-graph", figure=fig, config=graph_config)
        heat_row_child.append(graph)
    heat_row = dbc.Row(children=heat_row_child)

    out_fig = px.imshow(img_np_out,template="plotly_dark" )
    og_fig = px.imshow(img_np_in, template="plotly_dark")
    out_fig.update_layout(dragmode="zoom",
                      autosize=False,
                      margin=dict(l=0, r=0, b=0, t=10, pad=2),
                      width=900,
                      height=600
                      )

    og_fig.update_layout(dragmode="zoom",
                          autosize=False,
                          margin=dict(l=0, r=0, b=0, t=10, pad=2),
                          width=900,
                          height=600
                          )
    out_img = dcc.Graph(id="image-graph", figure=out_fig, config=graph_config)
    in_img = dcc.Graph(id="image-graph", figure=og_fig, config=graph_config)

    col = dbc.Col([out_img,in_img,heat_row])
    return col


loc = dcc.Location(id= 'job_url', refresh=False)
db_helper = Db_helper()
nav = Navbar("View Job")
columns = ["Type","Diameter","Area","X0", "Y0", "X1", "Y1"]
annotation_header = html.H4("Annotation Details")
annotation_refresh = dbc.Button("Refresh Table", id = "refresh-table")



#graph_copy = dcc.Store(id="graph-copy", data=fig),
job_store = dcc.Store(id = "job-store")
frame_store = dcc.Store(id ="frame-store")


image_view = html.Div(id= "image_view")
#create buffer to add space before header
buffer = html.Hr(style={"border": "20px"})
#create header
#header = html.H5("Viewing Job", style={"text-align": "center"})
#add separator after header
hr = html.Hr(style={"border": "6px solid light grey"})
job_header = dbc.Col(id = "job_header")
frame_row = dbc.Col(id = 'frame-row')
frame_overview = dbc.Col(id = 'frame-overview')
#frame_pore_table = dbc.Col(id = 'pore_table')
frame_details = dbc.Col(id = 'frame_details')
row_1l = dbc.Row(id="row_1l",children=[job_header,frame_row,frame_overview])
row_2l = dbc.Row(id="row_2l",children=[frame_details])
col_1l = dbc.Col([
        row_1l,
        row_2l
        ],
        width={'size':5,'offset':0.5})


img_selector_row = dbc.Row([
    html.Div(id = "img-info"),
    dcc.Dropdown(
                id = 'img-select',
                options=[],
                clearable=False,
                style = {'color': 'black','width':'120px'},
            )
])
data_imgs = html.Div(id = 'data-imgs')
col_2r = dbc.Col(children=[img_selector_row,image_view])
annotations_store = dcc.Store(id = "annotations-store")
fig_store = dcc.Store(id = 'fig-store')
job_data = dbc.Row(id = 'job_data',children=[col_1l,col_2r])
index_store = dcc.Store(id = 'index-store', data=0)
layout = html.Div(id="job_view", children = [
    loc,
    nav,
    buffer,
    job_data,
    job_store,
    frame_store,
    index_store,
    annotations_store,
    data_imgs
])


@app.callback(Output('img-info','children'),
              Input('frame-store','data'),
              State('index-store','data'))
def update_selector_row(frame_dic,index):
    count = len(frame_dic["image_data_ls"])
    img_str = "Image :" + str(frame_dic["image_data_ls"][index]['img_name']) + str(index + 1) + "/" + str(count)
    title = html.H5(img_str)
    return title

@app.callback(Output('img-select','options'),
              Output('img-select','value'),
              Input('frame-store','data'),
              prevent_initial_call=True)
def update_img_selector(frame):
    print("img_selector updated")
    options = [{'label':img["img_name"], 'value':img["img_path"]}
               for img in frame["image_data_ls"]]
    return options,frame["image_data_ls"][0]['img_path']


@app.callback(
    Output('job_header','children'),
    Output('job-store','data'),
    Input('job_url', 'pathname'),
)
def update_content(pathname):
    if pathname is not None and 'id' in pathname:

        #print("output for job id :", pathname[8:])
        jb = db_helper.fetch_job(pathname[8:])
        for frame in jb['frame_data_ls']:
            print("frame name:", frame['frame_name'])
        job_header_card = dbc.Card(dbc.CardBody([
            html.H5("Job Name: " + jb["job_name"],className='card-title'),
            html.H6("Select frame:"),
            dcc.Dropdown(
                id = 'frame-select',
                options=[
                    {'label':frame["frame_name"], 'value':frame["frame_name"]} for frame in
                    jb["frame_data_ls"]],
                clearable=False,
                style = {'color': 'black'}

            ),
            hr,
            dbc.Button("Delete Job", id='del-job',key= jb["job_id"]),
            ]),
            color='info',
            inverse=True,
            style = {"border-radius":"8px",'width':'200px'},
        )
        return job_header_card,jb
    else:
        return dash.no_update



@app.callback(
    Output('frame-row', 'children'),
    Output('frame-store','data'),
    Input('frame-select','value'),
    State('job-store','data'),
    )
def update_frame_cell(value,data):
    print("type of job_store", type(data))
    i=0
    j = 0

    while(i<len(data['frame_data_ls'])):
        frame = data['frame_data_ls'][i]
        if value == frame["frame_name"]:
            print("found frame_name")
            j = i
            i = len(data['frame_data_ls'])
        i = i+1
    frame= data["frame_data_ls"][j]

    num_str = "# of Img:" + str(len(frame['image_data_ls']))
    thresh_str = "Thresh Value: " + str(frame['thresh'])
    #thesh_type_str = "Alt thresh" + str(frame)
    scale_str = "Scale: " + str(frame['scale']) + " microns/px"
    card = dbc.Card([
        dbc.CardHeader(("Frame: " + frame['frame_name'])),
        html.P(num_str),
        html.P(thresh_str),
        html.P(scale_str)
        ]
    )
    return card,frame


@app.callback(
    Output('frame-overview','children'),
    Input('frame-store','data'),
    prevent_initial_call=True
    )
def update_frame_overview(frame_dic):
    pore_header = html.H4("Porosity Overview: ", frame_dic["frame_name"])
    pore_table = create_frame_pore_table(frame_dic)
    pore_avg = html.H5("Average Porosity: " + str(round(frame_dic['avg_pore'],4)))
    return [pore_header,pore_table,pore_avg]



@app.callback(Output('data-imgs','children'),
              Input('frame-store','data'))
def update_data_imgs(frame_dic):
    print("UPDATE DATA IMGS CALLED")
    data_imgs = show_datas(frame_dic)
    return [data_imgs]



@app.callback(
    Output('frame_details','children'),
    Input('frame-store','data'),
    prevent_initial_call=True
    )
def update_frame_view(frame_dic):
    if len(frame_dic)==0:
        return dash.no_update

    large_table = create_frame_area_table(frame_dic)
    large_header = html.H4("Largest Pores of Frame: ", frame_dic["frame_name"])
    hole_header = html.H4("Largest Holes of Frame")
    hole_table = create_frame_hole_table(frame_dic)
    pore_avg = frame_dic["avg_pore"]
    pore_str = "Average Porosity of Frame" + str(pore_avg)
    pore_summary = html.H4(pore_str)
    hist = show_histogram(frame_dic['hist'],frame_dic['hist_bins'])

    return dbc.Row([dbc.Col([large_header,
                             large_table,
                             hole_header,
                             hole_table,
                             hist,]),])


@app.callback(
    Output('image_view','children'),
    Input('img-select','value'),
    prevent_initial_call=True
    )
def update_image_view(path):
    return dbc.Col([update_view_image(path)])


@app.callback(
    Output('url','pathname'),
    Input("del-job",'n_clicks'),
    State("del-job",'key'),
    prevent_initial_call=True
)
def del_job(n_clicks,key):
    if n_clicks is None or type(n_clicks)==type(None) or n_clicks==0:
        return dash.no_update
    elif type(n_clicks) == type(1) and n_clicks>0:
        db_helper.delete_job(key)
        return "/"
    return dash.no_update


STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')


@app.server.route('/static/<resource>')
def serve_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)

# @app.callback(
#     Output("annotations-table", "data"),
#     Input("image-graph", "relayoutData"),
#     Input("refresh-table", "n_clicks"),
#     prevent_initial_call=True,
# )
# def on_new_annotation(relayout_data,n_clicks):
#     if "shapes" in relayout_data:
#         shape_cols = []
#         for shape in relayout_data["shapes"]:
#             print(shape)
#             if "editable" in shape.keys():
#                 row = shape_to_table_row(shape)
#                 shape_cols.append(row)
#         return shape_cols
#
#         #return json.dumps(relayout_data["shapes"], indent=2)
#     else:
#         return dash.no_update

# @app.callback(
#     Output("annotations-table", "data"),
#     Input("refresh-table", 'n_clicks'),
#     State("image-graph","relayoutData")
# )
# def refresh_table(n_clicks,relayout_data):
#     if n_clicks is None or n_clicks == 0:
#         return []
#     else:
#         shape_cols = []
#         for shape in relayout_data["shapes"][2:]:
#             print(shape)
#
#             row = shape_to_table_row(shape)
#             shape_cols.append(row)
#         return shape_cols


# @app.callback(
#     Output("image-graph","figure"),
#     Input("add-circle", "n_clicks"),
#     Input("new-radius", "value"),
#     #State("graph-copy","data")
# )
# def add_template_circle(n_clicks,r):
#     #print(type(data),"of data")
#
#
#     if n_clicks is None or n_clicks ==0:
#         return dash.no_update
#     else:
#         #fig = data
#         return generate_template_circle(r)
