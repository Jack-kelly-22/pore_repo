import dash
from dash_bootstrap_components import themes

app = dash.Dash(__name__,external_stylesheets=[themes.DARKLY],suppress_callback_exceptions=True)
server = app.server