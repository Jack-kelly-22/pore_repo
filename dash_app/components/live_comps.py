import dash_html_components as html
from dash_bootstrap_components import Table,Col
def create_pore_table(largest_areas,scale):
    table_header = [
        html.Thead(html.Tr([html.Th("Pore Size"),
                            html.Th("(x,y)"),
                            html.Th("Diameter of Largest Circle"),
                            html.Th("center")]
                           ))
    ]
    rows = [html.Tr([html.Td(area[1]),
            html.Td("(" + str(area[2]) + "," + str(area[3]) +")"),
            html.Td(round(area[5]* 2 * float(scale),2)),
            html.Td(str(area[4]))
            ]) for area in largest_areas[:10]]


    table_body = [html.Tbody(rows)]
    table = Table(table_header + table_body,
        bordered= True,
        dark = True,
        size = 'sm',
        striped = True,
        style={'padding':"2px"},
        )
    return table


def create_summary_table(porosity,largest_area,
                         largest_diam,warn,thresh,scale):

    table_label = html.H4("Summary"),

    table_header = [html.Thead(html.Tr([
        html.Th("Porosity"),
        html.Th("Largest Area"),
        html.Th("Largest Diameter"),
        html.Th("Threshold"),
        html.Th("Scale(microns/px)")
    ]))]
    rows = [html.Tr([
        html.Td(porosity),
        html.Td(largest_area[1]),
        html.Td(largest_diam[1] * 2 *  float(scale)),
        html.Td(thresh),
        html.Td(scale)

    ])]
    table_body = [html.Tbody(rows)]
    table = Table(table_header + table_body,
        bordered= False,
        dark = True,
        size = 'sm',
        striped = True,
        )

    col = Col([
        table_label,
        table
    ])
    return table


def create_hole_table(largest_holes,scale):

    table_header = [
        html.Thead(html.Tr([
                            html.Th("Diameter(microns)"),
                            html.Th("center(px)"),
                            html.Th("area(microns)",)]
                           ))
    ]
    rows = [html.Tr([
            html.Td(round(hole[1] * 2 * scale,2)),
            html.Td('( ' + str(hole[0][0]) + ' ' + str(hole[0][1]) + ' )'),
            html.Td(round((hole[1]*hole[1]) * 3.14 * scale * scale,2))
            ]) for hole in largest_holes[:10]]


    table_body = [html.Tbody(rows)]
    table = Table(table_header + table_body,
        bordered= True,
        dark = True,
        striped = True,
        style={'padding':"2px"},
        size = 'sm'
        )
    return table
