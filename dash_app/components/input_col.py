import dash_html_components as html
import dash_bootstrap_components as dbc

hr = html.Hr(style={'border-top':'3px dashed gray'})


def get_input_col(pre,job=False):
    fiber_choice = html.Div([
        html.H5("Fiber type"),
        dbc.Select(id=pre + "-fiber-type",
                   options=[
                       {"label": "Light fibers", "value": "light"},
                       {"label": "Dark fibers", "value": "dark"},
                   ],
                   value="dark"
                   )
    ])

    job_div = html.Div([
            html.H5("Job name"),
            dbc.Input("frame_name", placeholder="Enter a name for this Job", type="text"),
        ])

    thresh = html.Div(children=[
        html.H5("Adjust Threshold"),
        dbc.Input(id=pre + "-thresh", placeholder="default is 160", type="text", value='160'),
    ])

    warn = html.Div(children=[
        html.H5("Size to Alert On"),
        dbc.Input(id=pre + "-warn", placeholder="default is 5000", type="text", value='5000'),
    ])

    ignore = html.Div(children=[
        html.H5("Size to ignore"),
        dbc.Input(id=pre + "-ignore", placeholder="default is 20", type="text", value='20'),
    ])
    multi = html.Div([
        html.H5("Multi-color output"),
        dbc.Checkbox(id=pre + "-multi", ),
        dbc.Label(
            "Use Multi-Color",
            className="form-check-label",
        ),
    ])
    alt = html.Div([
        html.H5("Alternative threshold(local thresholding)"),
        dbc.Checkbox(id=pre +"-alt"),
        dbc.Label(
            "Use Alternative",
            className="form-check-label",
        ),
        dbc.Input(id=pre + "-alt-thresh", placeholder="around 55-78", type="text", value='68'),
    ])

    boarder = html.Div([
        dbc.Col([

            dbc.Row([
            dbc.Label("Crop boarder?",),
            dbc.Checkbox(id=pre+'-crop'),

        ]),
        dbc.Row([
            html.H5("Boarder size: "),
            dbc.Input(id=pre + '-boarder-size', value='10')
        ])
        ])
    ])

    scale = html.Div([
        html.H5("Scale(microns/pixel)"),
        dbc.Input(id=pre + "-scale", placeholder="default is 55", type="text", value='2.6'),
    ])

    num = html.Div([
        html.H5("Number or circles to draw per image"),
        dbc.Input(id=pre + "-number", placeholder="default is 50", type="text", value='50'),
    ])

    preview = dbc.Button("Preview image", id="preview-button", color="secondary")

    spreadsheet = html.Div([
        html.H5("Create Spreadsheet (not for preview images)"),
        dbc.Checkbox(id="spread"),
        ])


    run_button = dbc.Button("Run", id= pre +'-run')
    col_elems = [
        fiber_choice,
        hr,
        thresh,
        hr,
        alt,
        hr,
        multi,
        hr,
        scale,
        hr,
        boarder,
        hr,
        warn,
        hr,
        ignore,
        hr,
        num,
        hr,
        spreadsheet,
        hr,
        run_button
    ]
    if(job):
        col_elems.insert(0,job_div)
        col_elems.append(preview)
    col = dbc.Col(col_elems)

    return dbc.Container(children=[col])