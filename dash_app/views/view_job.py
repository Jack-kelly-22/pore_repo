import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_app.views.navbar import Navbar

#jb = fetch_job(job_id)

# nav = Navbar()
# #create buffer to add space before header
# buffer = html.Hr(style={"border": "15px"})
# #create header
# header = html.H5("View Results", style={"text-align": "center"})
# #add separator after header
# hr = html.Hr(style={"border": "6px solid light grey"})
#sub
#jb = fetch_job("9fcf1971b9f94f77a4fc956251fee84c_qqq")
#fb = jb["frame_data_ls"][0]
# print(jb)
# print("this is fb",fb)
# output = html.Div(id = 'output',children = [])
# job_header_card = dbc.Card(color = "info", children = [
#     dbc.CardHeader("Job Name: " + jb["job_name"]),
#     dbc.CardBody([
#         html.P("Job ID: " + jb["job_id"]),
#         html.P("Job type: " + str(jb["job_type"])),
#         html.P("Number of frames: " + str(len(jb["frame_data_ls"]))),
#     ]),
#     ],
#     style = {"border-radius":"20px"},
#     inverse= True)
#
# frame_header_card = dbc.Card(color = "warning", children = [
#     dbc.CardHeader("Frame Name: " + jb["job_name"]),
#     dbc.CardBody([
#         html.P("Frame ID: " + fb["frame_id"]),
#         html.P("Job type: " + fb["frame_name"]),
#         html.P("Job type: " + fb["frame_name"]),
#         html.P("# of images in frame: " + str(len(fb["image_data_ls"]))),
#         dbc.Button("See Details")
#     ]),
#     ],
#     style = {"border-radius":"20px"},
#     inverse= True)
# i = 0
# def create_frame_list_item(frame_dict):
#     print("creating new frame list item")
#     info_string = "frame_id: " + frame_dict["frame_id"] + "\n frame path: " + frame_dict["frame_path"]
#     item = dbc.ListGroupItem(id = frame_dict["frame_name"],
#         children = [
#             dbc.ListGroupItemHeading(frame_dict["frame_name"]),
#             dbc.ListGroupItemText(info_string),
#             #dbc.ListGroupItemHeading(frame_dict["frame_name"]),
#             html.Div(id = {'type':'list-button', 'index': 0},
#                 children = [dbc.Button("View frame", id = frame_dict["frame_id"])],
#                 style={"text-align": "rigth"})
#         ]
#     )
#     #i = i + 1
#     return item
#
# frame_list_header = html.H3("Frames in Job")
#
#
#
# def get_frame_list(job_id):
#     child = []
#     for frame in job_id["frame_data_ls"]:
#         print("createing list item for frame ")
#         child.append(create_frame_list_item(frame))
#
#     frame_list = dbc.ListGroup(children = child)
#     return frame_list
#
# def create_job_header_card(job_dic):
#     card = dbc.Card(color = "info", children = [
#         dbc.CardHeader("Job Name: " + job_dic["job_name"]),
#         dbc.CardBody([
#             html.P("Job ID: " + job_dic["job_id"]),
#             html.P("Job type: " + str(job_dic["job_type"])),
#             html.P("Number of frames: " + str(len(job_dic["frame_data_ls"]))),
#         ]),
#     ],
#     style = {"border-radius":"20px"},
#     inverse= True)
#     return card
#
#
# def View_Job(job_id,db_ut):
#     job_dic = db_ut.fetch_job("9fcf1971b9f94f77a4fc956251fee84c_qqq")
#     print("starting view job")
#     frame_list = get_frame_list(job_dic)
#     job_header_card = create_job_header_card(job_dic)
#     row =html.Div([
#         dbc.Row(
#             [
#                 dbc.Col(children = [job_header_card, frame_header_card],
#                     width={"size": 4, "order": 0},
#                 ),
#                 dbc.Col(children = [
#                     frame_list_header,
#                     frame_list,
#                     html.Div(id = {'type': "dynamic-out", 'index': '0'}, children = []),
#
#                 ]),
#             ]
#         ),
#     ])
#     image_sec = html.Div(id = "img-sec")
#     layout = html.Div([
#         nav,
#         html.Br(),
#         header,
#         hr,
#         row,
#         hr,
#
#
#     ])
#     return layout