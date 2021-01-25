from pandas import DataFrame
from plotly.express import bar
import plotly.express as px
from dash_core_components import Graph
from dash_bootstrap_components import Row, Col
from skimage.io import imread
def show_histogram(hist,hist_bins):
    #print(px.data.tips())
    df = DataFrame({'bins':hist_bins[1:],'counts':hist})
    fig = bar(df,x="bins",y='counts',text='counts',
                 title='Pore Size Distribution',
                 template = "plotly_dark")
    hist_graph = Graph(id = 'hist-graph',figure=fig)
    return hist_graph


def show_datas(frame_dic):
    print("PATH",frame_dic['hist_area_img_path'])
    #load images into figure objects
    hist_area_fig = px.imshow(imread(frame_dic['hist_area_img_path']),template="plotly_dark")
    hist_diam_fig = px.imshow(imread(frame_dic['hist_diam_img_path']),template="plotly_dark")
    disk_area_fig = px.imshow(imread(frame_dic['disk_area_img_path']),template="plotly_dark")
    disk_pore_fig = px.imshow(imread(frame_dic['disk_pore_img_path']),template="plotly_dark")
    #adjust layout of figure objects
    hist_area_fig.update_layout(autosize=True,margin=dict(l=0, r=0, b=0, t=10, pad=2))
    hist_diam_fig.update_layout(autosize=True, margin=dict(l=0, r=0, b=0, t=10, pad=2))
    disk_area_fig.update_layout(autosize=True, margin=dict(l=0, r=0, b=0, t=10, pad=2))
    disk_pore_fig.update_layout(autosize=True, margin=dict(l=0, r=0, b=0, t=10, pad=2))

    hist_area_graph = Graph(id = 'hist-graph',figure=hist_area_fig)
    hist_diam_graph = Graph(id='hist-graph', figure=hist_diam_fig)
    disk_area_graph = Graph(id='hist-graph', figure=disk_area_fig)
    disk_pore_graph = Graph(id='hist-graph', figure=disk_pore_fig)

    hist_row = Row(id='hist-row', children=[hist_area_graph, hist_diam_graph])
    disk_row = Row(id='disk-row', children=[disk_area_graph, disk_pore_graph])
    col = Col(id='data-col', children=[hist_row, disk_row])
    return col