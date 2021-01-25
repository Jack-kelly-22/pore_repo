import dash_html_components as html
import dash_bootstrap_components as dbc
from utils.input_utils import get_folder_checks
def get_file_col():
    header = html.H3("Select Folders")
    checks = get_folder_checks()
    return dbc.Col([header,checks])