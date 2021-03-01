import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash_app.app import app
from dash_app.views.navbar import Navbar
import dash_bootstrap_components as dbc
from dtypes.db_helper import Db_helper
from dash_app.components.table_comps import *
from dash_app.components import annotation_comps
from utils.graph_utils import *
import dash_table as dt
import plotly.express as px
from dtypes.subImage import *
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





loc = dcc.Location(id= 'job_url', refresh=False)
db_helper = Db_helper()
nav = Navbar("View Job")
columns = ["Type","Diameter","Area","X0", "Y0", "X1", "Y1"]
annotation_header = html.H4("Annotation Details")
annotation_refresh = dbc.Button("Refresh Table", id = "refresh-table")

job_store = dcc.Store(id = "job-store")
frame_store = dcc.Store(id ="frame-store")
graph_config = {
    "modeBarButtonsToAdd": [

        "drawclosedpath",
        "drawcircle",
        "drawrect",
        "eraseshape",
    ],
}





@app.callback(
    dash.dependencies.Output("annotation-thresh-label", 'children'),
    [dash.dependencies.Input('annotation-thresh', 'value')])
def update_output(value):
    return ''.format(value)

image_view = dbc.Col(id= "image_view",children=[
    dcc.Graph(id="image-out-view",config=graph_config),
    annotation_comps.create_annotation_card()

])
#create buffer to add space before header
buffer = html.Hr(style={"border": "20px"})


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
        row_2l,

        ],
        width={'size':5,'offset':0.5})


img_selector_row = dbc.Row([
    html.Div(id = "img-info"),
    dcc.Dropdown(
                id = 'img-select',
                options=[],
                clearable=False,
                style = {'color': 'black','width':'120px'},
            ),
    dbc.Button("Toggle Original", id='toggle-img',)
])


data_imgs = html.Div(id='data-imgs')
col_2r = dbc.Col(children=[img_selector_row,image_view])
annotations_store = dcc.Store(id="annotations-store")
fig_store = dcc.Store(id='fig-store')
job_data = dbc.Row(id = 'job_data',children=[col_1l,col_2r])
index_store = dcc.Store(id='index-store', data=0)
constants_store = dcc.Store(id='constants-store')
subImage_store = dcc.Store(id="subImage-store")
layout = html.Div(id="job_view", children = [
    loc,
    nav,
    buffer,
    job_data,
    job_store,
    frame_store,
    index_store,
    annotations_store,
    constants_store,
    data_imgs,
    subImage_store
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
    i=0
    j=0

    while(i<len(data['frame_data_ls'])):
        frame = data['frame_data_ls'][i]
        if value == frame["frame_name"]:
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
    return card,frame,


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
                             hist
                             ]),])

@app.callback(
    Output('image-out-view','figure'),
    Output('index-store','data'),
    Input('img-select','value'),
    Input('toggle-img','n_clicks'),
    State('frame-store','data'),
    prevent_initial_call=True
    )
def update_image_out_view(path,n_clicks,frame_dic):
    print("UPDATED IMAGE")
    if(n_clicks is not None and n_clicks%2!=0):
        path1 = path[:-6] + 'g.png'
    else:
        path1=path
    img_np_out = io.imread(path1)

    i=0
    found= False
    print("path:",path)
    print('frame',frame_dic)
    if(frame_dic is not None):

        while(i<len(frame_dic['image_data_ls']) and not found):
            if path == frame_dic['image_data_ls'][i]["img_path"]:
                found = True
                print("found")
            else:
                i+=1


    out_fig = px.imshow(img_np_out, template="plotly_dark")
    out_fig.update_layout(dragmode="zoom",
                          autosize=False,
                          margin=dict(l=0, r=0, b=0, t=10, pad=2),
                          width=600,
                          height=400
                          )
    return out_fig,i

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


@app.callback(
    #Output("update-annotation-button", "n_clicks"),
    Output("subImage-store",'data'),
    Input("image-out-view", "relayoutData"),
    State("frame-store",'data'),
    State("index-store",'data'),
    State("update-annotation-button", 'n_clicks'),
    State("annotation-circles","value",),
    State("annotation-thresh","value'"),

    prevent_initial_call=True,
)
def on_new_annotation(relayout_data,frame_dic,i,n,num,thresh):
    if "shapes" in relayout_data:
        print("NEW ANNOTATION")
        last_shape = relayout_data["shapes"][-1]
        # shape coordinates are floats, we need to convert to ints for slicing
        x0, y0 = int(last_shape["x0"]), int(last_shape["y0"])
        x1, y1 = int(last_shape["x1"]), int(last_shape["y1"])
        img = frame_dic["image_data_ls"][i]["img_path"]
        subImage={}
        #img = io.imread(img)
        #img = img[y0:y1, x0:x1]
        #subImage = create_subImage(img,frame_dic,x0,x1,y0,y1,num,thresh)
        #sub_table = create_frame_hole_table(subImage,3)
        subImage['x0'] = x0
        subImage['x1'] = x1
        subImage['y0'] = y0
        subImage['y1'] = y1
        subImage['i'] = i
        subImage['img_path']= frame_dic["image_data_ls"][i]["img_path"]

        # return 1,#subImage
        return subImage


    else:
        return dash.no_update





@app.callback(
    dash.dependencies.Output("annotation-view", 'figure'),
    dash.dependencies.Output("annotation-table", 'children'),
    [dash.dependencies.Input('update-annotation-button', 'n_clicks'),
     dash.dependencies.State('annotation-thresh', 'value'),
     dash.dependencies.State('subImage-store', 'data'),
     State('annotation-circles','value'),
     State('frame-store', 'data'),
     # State('annotation-circles','value'),
     # State('annotation-multi','value')
     ],
    prevent_initial_call=True)
def update_annotation(n_clicks,thresh,subImage,num,frame_dic,):
    if n_clicks is None or n_clicks==0:
        return dash.no_update
    frame_dic['thresh'] = float(thresh)
    frame_dic['crop']= False
    x0, y0 = int(subImage["x0"]), int(subImage["y0"])
    x1, y1 = int(subImage["x1"]), int(subImage["y1"])
    img = frame_dic["image_data_ls"][subImage['i']]["img_path"]
    img = io.imread(img[:-6]+'g.png')
    img = img[y0:y1, x0:x1]

    subImage = create_subImage(img,frame_dic,
                               x0=x0,x1=x1,y0=y0,y1=y1,
                               thresh=int(thresh),num_circles=int(num))
    sub_table = create_frame_hole_table(subImage)
    fig = px.imshow(subImage['out_img'])
    fig.update_layout(dragmode="zoom",
               autosize=True,
               margin=dict(l=0, r=0, b=0, t=10, pad=2),
               )
    return fig,sub_table

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



