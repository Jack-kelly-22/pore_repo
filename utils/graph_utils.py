import time


def format_float(f):
    return "%.2f" % (float(f),)


def time_passed(start=0):
    return round(time.mktime(time.localtime())) - start

def shape_data_remove_timestamp(shape):
    """
    go.Figure complains if we include the 'timestamp' key when updating the
    figure
    """
    new_shape = dict()
    for k in shape.keys() - set(["timestamp"]):
        new_shape[k] = shape[k]
    return new_shape


def coord_to_tab_column(coord):
    return coord.upper()

def annotations_table_shape_resize(annotations_table_data, fig_data):
    """
    Extract the shape that was resized (its index) and store the resized
    coordinates.
    """
    #debug_print("fig_data", fig_data)
    #debug_print("table_data", annotations_table_data)
    for key, val in fig_data.items():
        shape_nb, coord = key.split(".")
        # shape_nb is for example 'shapes[2].x0': this extracts the number
        shape_nb = shape_nb.split(".")[0].split("[")[-1].split("]")[0]
        # this should correspond to the same row in the data table
        # we have to format the float here because this is exactly the entry in
        # the table
        annotations_table_data[int(shape_nb)][
            coord_to_tab_column(coord)
        ] = format_float(fig_data[key])
        # (no need to compute a time stamp, that is done for any change in the
        # table values, so will be done later)
    return annotations_table_data


def shape_to_table_row(sh):
    d= "None"
    if(sh['type']=="circle"):
        d = str(sh["x1"] - sh["x0"])


    return {
        #"Type": type_dict[sh["line"]["color"]],
        "Type": sh["type"],
        "Diameter" : d,
        "X0": format_float(sh["x0"]),
        "Y0": format_float(sh["y0"]),
        "X1": format_float(sh["x1"]),
        "Y1": format_float(sh["y1"]),
    }

def shape_cmp(s0, s1):
    """ Compare two shapes """
    return (
        (s0["x0"] == s1["x0"])
        and (s0["x1"] == s1["x1"])
        and (s0["y0"] == s1["y0"])
        and (s0["y1"] == s1["y1"])
        and (s0["line"]["color"] == s1["line"]["color"])
    )

def default_table_row():
    return {
        "Type": "Default",
        "X0": format_float(10),
        "Y0": format_float(10),
        "X1": format_float(20),
        "Y1": format_float(20),
    }

def index_of_shape(shapes, shape):
    for i, shapes_item in enumerate(shapes):
        if shape_cmp(shapes_item, shape):
            return i
    raise ValueError  # not found


def shape_in(se):
    """ check if a shape is in list (done this way to use custom compare) """
    return lambda s: any(shape_cmp(s, s_) for s_ in se)

def table_row_to_shape(tr):
    return {
        "editable": True,
        "xref": "x",
        "yref": "y",
        "layer": "above",
        "opacity": 1,
        #"line": {"color": color_dict[tr["Type"]], "width": 4, "dash": "solid"},
        "line": {"width": 4, "dash": "solid"},
        "fillcolor": "rgba(0, 0, 0, 0)",
        "fillrule": "evenodd",
        "type": "rect",
        "x0": tr["X0"],
        "y0": tr["Y0"],
        "x1": tr["X1"],
        "y1": tr["Y1"],
    }


def generate_template_circle(r):
    return {
        "editable": True,
        "xref" : "x",
        "yref" : "y",
        "layer": "above",
        "opacity" : 0.5,
        "line": {
          "color": "#139",
          "width": 4,
          "dash": "solid"
        },
        "fillcolor": "rgba(0, 0, 0, 0)",
        "fillrule": "evenodd",
        "type": "rect",
        "x0": 100,
        "y0": 100,
        "x1": 150,
        "y1": 250,

    }