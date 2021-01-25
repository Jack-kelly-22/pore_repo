def remove_z_set(coord_set):
    x_y = set()
    for coord in coord_set:
        x_y.add((coord[1],coord[0]))
    return x_y

def check_pt(coord, middle, inc_area,coords):
    #print("checlomg x:", coord[0],"y: ", coord[1])
    if coord in inc_area:
        return True
    if (coord in coords):
        return True
    if(coord[0]>600 or coord[1]>800):
        return False
    return False
#
# def circle_pts_in_coords(circle_pts,coords):
#     '''determines if circle_pts are subset of coords'''
#     if type(circle_pts) is not set:
#         circle_pts = circle_pts(set)
#     if type(coords) is not set:
#         coords = coords(set)
#     if circle_pts.issubset(coords)


def check_circle(circle_pts,area_pts):
    if(circle_pts.issubset(area_pts)):
        return True
    return False