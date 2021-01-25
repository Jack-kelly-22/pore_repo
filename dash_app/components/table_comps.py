import dash_html_components as html
from dash_bootstrap_components import Table
def sort_areas(frame_dic):
    """returns a list of tuples
    0: image_name
    1: area size
    2: area x
    3: area y"""
    area_ls = []
    for image in frame_dic["image_data_ls"]:
        #print("ty:",type(image),image)
        if(image != 'EMPTY_IMAGE_LS'):
            for entry in image["img_largest_areas"]:
                val = (entry[0],int(entry[1]),entry[2],entry[3],entry[4],entry[5])
                area_ls.append(val)

    area_ls = sorted(area_ls,key = lambda tup: int(tup[1]))
    #print("sorted areas:",area_ls)
    area_ls.reverse()
    return area_ls


def sort_holes(frame_dic):
    hole_ls = []
    for image in frame_dic["image_data_ls"]:
        if (image != 'EMPTY_IMAGE_LS'):
            for entry in image["largest_holes"]:
                hole_ls.append([entry[0],int(entry[1]),image['img_name']])
    hole_ls = sorted(hole_ls,key = lambda tup:int(tup[1]))
    hole_ls.reverse()
    return hole_ls

def create_frame_area_table(frame_dic):
    area_ls = sort_areas(frame_dic)
    table_header = [
        html.Thead(html.Tr([html.Th("Pore Size"),
                            html.Th("Image Name"),
                            html.Th("(x,y)"),
                            html.Th("Diameter of Largest Circle"),
                            html.Th("center")]
                           ))
    ]
    rows = []
    if(len(area_ls)==0):
        return []
    for area in area_ls[:5]:
        px_str = ' (' + str(area[5]) + 'pixels' + ')'
        row = html.Tr([html.Td(int(area[1])),
            html.Td(area[0]),
            html.Td("(" + str(area[2])+ "," + str(area[3]) +")"),
            html.Td(str(round(area[5]*2*float(frame_dic["scale"]),2)) +px_str),
            html.Td(str(area[4]))
            ])

        rows.append(row)
    table_body = [html.Tbody(rows)]
    table = Table(table_header + table_body,
        bordered= True,
        dark = True,
        striped = True,
        size = 'sm')
    return table


def create_frame_pore_table(frame_dic):
    pore_ls = []
    name_ls = []
    for image in frame_dic["image_data_ls"]:
        if(image!="EMPTY_IMAGE_LS"):
            pore_ls.append(image["pores"])
            name_ls.append(image["img_name"])
    table_header = [
        html.Thead(html.Tr([
                            html.Th("Image Name"),
                            html.Th("Porosity"),]
                           ))
    ]
    rows = []
    if(len(pore_ls)==0):
        return []
    i =0
    while i< len(pore_ls):
        row = html.Tr([
            html.Td(name_ls[i]),
            html.Td(round(pore_ls[i],4)),
            ])
        rows.append(row)
        i=i+1

    table_body = [html.Tbody(rows)]
    table = Table(table_header + table_body,
        bordered= True,
        dark = True,
        striped = True,
        size = 'sm')
    return table


def create_frame_hole_table(frame_dic):
    holes = sort_holes(frame_dic)
    scale = float(frame_dic['scale'])
    table_header = [
        html.Thead(html.Tr([
                            html.Th("Diameter(microns)"),
                            html.Th("center(px)"),
                            html.Th("area(microns)"),
                            html.Th("Image name")]
                           ))
    ]
    rows = [html.Tr([
            html.Td(round(hole[1] * 2 * scale,2)),
            html.Td('( ' + str(hole[0][0]) + ' ' + str(hole[0][1]) + ' )'),
            html.Td(round((hole[1]*hole[1]) * 3.14 * scale * scale,2)),
            html.Td(hole[2])
            ]) for hole in holes[:10]]


    table_body = [html.Tbody(rows)]
    table = Table(table_header + table_body,
        bordered= True,
        dark = True,
        striped = True,
        style={'padding':"2px"},
        size = 'sm'
        )
    return table