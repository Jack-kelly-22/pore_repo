import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

graph_config = {
    "modeBarButtonsToAdd": [

        "drawclosedpath",
        "drawcircle",
        "drawrect",
        "eraseshape",
    ],
}

def create_annotation_card():
    annotation_card = dbc.Card(id = 'annotation-card',children=[
        dbc.CardBody(
            [
                dbc.Container([
                dbc.Col([
                    html.H4("Annotation", ),
                    dcc.Graph(id="annotation-view", config=graph_config,),
                    dbc.Button("Update annotation",
                               id="update-annotation-button",
                               color="primary"),
                ]),
                dbc.Col([
                    html.H4("Settings"),
                    create_thresh_row(),
                    html.H4("# of circles"),
                    dbc.Input(id="annotation-circles", value ='5')
                ]),
                dbc.Col([html.Div(id='annotation-table')])
            ])
            ],
        ),
    ],
        style={'width': '600px'}
    )
    return annotation_card

def create_thresh_row(init_thresh=130):
    thresh_row = dbc.Row([
        html.H5("Threshold: "),
        dbc.Input(id='annotation-thresh', min=10, max=300, step=1,
                  style={'width': '100px'}, value= init_thresh),
        # dbc.Select(id="annotation-multi",
        #             options=[
        #                 {"label": "True", "value": True},
        #                 {"label": "False", "value": True},
        #             ]
        #         )
    ])
    return thresh_row