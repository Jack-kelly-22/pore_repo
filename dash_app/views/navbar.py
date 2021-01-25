import dash_bootstrap_components as dbc
import dash_html_components as html
def Navbar(header):
    nav =dbc.NavbarSimple(
        children = [
            dbc.NavItem(dbc.NavLink("Previous Jobs", href="/prev-jobs")),
            dbc.NavItem(dbc.NavLink("New Job", href="/new-job")),
            #dbc.NavItem(dbc.NavLink("Edit Job", href="/edit-job")),

        ],
        brand='Pore Software',
        brand_href="/ps",
        sticky="top",
        color = "primary",
        )

    return nav