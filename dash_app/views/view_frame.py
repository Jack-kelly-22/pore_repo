
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_app.views.navbar import Navbar
import base64
import plotly.express as px
# from utils.sql_utils import fetch_frame, fetch_image
# #jb = fetch_job(job_id)
#
#
# def sort_areas(frame_dic):
#     """returns a list of tuples
#     0: image_name
#     1: area size
#     2: area x
#     3: area y"""
#     area_ls = []
#     for image in frame_dic["image_data_ls"]:
#         for entry in image["areas"]:
#             val = (entry[0],int(entry[1]),entry[2],entry[3])
#             area_ls.append(val)
#
#     area_ls = sorted(area_ls,key = lambda tup: tup[1])
#     return area_ls
#
#
# def create_area_table(frame_dic):
#     area_ls = sort_areas(frame_dic)
#     table_header = [
#         html.Thead(html.Tr([html.Th("Pore Size"),html.Th("Image Name"),html.Th("(x,y)"),html.Th("Area"),html.Th("equivalent diameter"),html.Th("ecentricity")]))
#     ]
#     rows = []
#     for area in area_ls:
#         row = html.Tr([html.Td(int(area[1])),
#             html.Td(area[0]),
#             html.Td("(" + str(area[2])+ "," + str(area[3]) +")"),
#             html.Td(area[3]),
#             #html.Td(area[4]),
#             #html.Td(area[5])
#             ])
#         rows.append(row)
#
#     table_body = [html.Tbody(rows)]
#     table = dbc.Table(table_header + table_body,
#         bordered= True,
#         dark = True,
#         striped = True)
#     return table
#
# def View_Image(im_dic):
#     print("view single image:", type(im_dic))
#     print(im_dic)
#     image_filename = '/Users/jackkelly/jkdev/dash_vs/local/job-data/qqq/frame_0/image2_THRESH_73.0_out.png' # replace with your own image
#     encoded_image = base64.b64encode(open(image_filename, 'rb').read())
#     """
#     app.layout = html.Div([
#         html.Img(src='data:image/png;base64,{}'.format(encoded_image))"""
#     card = dbc.Card(color = "info", children = [
#         dbc.CardImg(src='data:image/png;base64,{}'.format(encoded_image.decode()), top= True  ),
#         dbc.CardHeader(im_dic["img_name"]),
#         #html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
#         #dbc.CardBody([
#         #    html.P("Porosity: " + str(im_dic["pores"])),
#         #]),
#     ],
#     style = {"border-radius":"20px"},
#     inverse= True)
#     return card
#
# def View_Images(im_dic_ls):
#     card_ls = []
#     for image in im_dic_ls:
#         print(type(image))
#         card = View_Image(image)
#         card_ls.append(card)
#     images_header = html.H4("Images in frame:")
#     #im_div = html.Div([images_header,card_ls])
#     return card_ls
#
#
# def create_frame_area_hist(frame_dic):
#     frame_areas = []
#     for img in frame_dic["image_data_ls"]:
#         for area in img["all_areas"]:
#             frame_areas.append(area)
#     df = pd.DataFrame(frame_areas, columns=["a"])
#     fig = px.histogram(df, x = "area")
#     return fig
# def View_Frame(id):
#     if(id!=0):
#         frame_dic = fetch_frame(id)
#         frame_header = html.H3("Summary of " + frame_dic["frame_name"])
#         area_table = create_area_table(frame_dic)
#         #change this later!!
#         #hist = create_frame_area_hist(frame_dic)
#         image_sect = View_Images(frame_dic["image_data_ls"])
#         graph = dcc.Graph(id = "hist",)
#         layout = html.Div([
#             frame_header,
#             area_table,
#             image_sect[0],
#             graph
#         ])
#         return layout
