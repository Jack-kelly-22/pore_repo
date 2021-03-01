def remove_z_set(coord_set):
    x_y = set()
    for coord in coord_set:
        x_y.add((coord[1],coord[0]))
    return x_y

#z
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
    else:
        if(len(circle_pts-area_pts)<5):
            return True
    return False