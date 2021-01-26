from skimage.segmentation import chan_vese
from numpy import percentile,histogram,linalg,copy
import cv2
from skimage import exposure
from skimage.filters import gaussian,threshold_isodata
from skimage.color import rgb2gray
from numpy import uint8
from porespy.metrics import porosity
from utils import coord_utils
from skimage.draw import disk
from utils import data_utils
from tensorflow import image as tfImage
from utils.filters_utils import scalar_transform
from pandas import DataFrame
from skimage.filters import threshold_sauvola,threshold_local,threshold_otsu
from skimage.filters.rank import enhance_contrast_percentile
from PIL import ImageEnhance


def adjust_exposure(image,lower = 1, high = 99):
    p2,p98 = percentile(image,(lower,high))
    return exposure.rescale_intensity(image)


def get_all_areas(regions):
    areas = []
    for region in regions:
        area = region["area"]
        areas.append(area)
    #print("about to retrun areas: ", areas[:10])
    return areas

def get_real_area(region):
    area_set = {(1, 0)}
    #print("region area:", str(region.area))
    for pt in region.coords:
        x = pt[1]
        y = pt[0]
        #z = pt[2]
        area_set.add((x, y))
    #print("returned area = ", len(area_set))
    return len(area_set) - 1

def get_porosity(img_seg):
    pore = porosity(img_seg)
    return pore

def get_largest_areas(regions,image_data):
    # dataframe = ps.metrics.props_to_DataFrame(regions)
    largest_pores = []
    #largest_pores_coords =[]
    print("gonna sort ",len(regions))
    ig = float(image_data.ignore_size)
    #regions = filter(lambda: region.area<image_data.ignore_size,regions)
    regions = [region for region in regions if region.area>ig]
    #regions = sorted(regions,key = lambda tup: t)
    regions.sort(key=lambda reg:reg["area"])
    largest_reg = []


    if len(regions)>100:
        regions = regions[-image_data.num_circles:]
    regions.reverse()
    largest_circles = []
    i = 0
    print("len of regions:", len(regions))
    for region in regions:
        y, x, = region["centroid"]
        coords = region["coords"]
        print("centroid:", x,y)
        coords = coord_utils.remove_z_set(coords)
        center,r = get_largest_circle_in_region(coords,centroid=(int(x),int(y))) #finds largest incribed circle
        largest_circles.append([center,r,image_data.name])
        center = (center[0], center[1])
        largest_pores.append(
            [image_data.name,
             int(region.area * (image_data.scale_factor * image_data.scale_factor)),
             (x // 1),
             (y // 1),
             center,
             r
             ])
        print("reg:" + str(i) + '/' + str(len(regions)) )
        i = i + 1
    largest_circles.sort(key= lambda x: x[1],reverse=True)
    #largest_circles.reverse()
    largest_pores.sort(key = lambda x:x[1],reverse=True)
    
    return largest_pores,regions,largest_circles

def get_thresh_image(image, constants):
    if constants["use_alt"]:
        print("USED ALT THRESH")
        img_seg = get_alt_thresh_image(image, constants["alt_thresh"],constants['fiber_type'])
    else:
        #image = rgb2gray(image)
        print("start regular thresh")
        img_seg = get_reg_thresh_image(image, constants["thresh"],constants['fiber_type'])
    return img_seg


def get_alt_thresh_image(image,alt_thresh,fiber):

    #image = tfImage.adjust_saturation(image,2.6)
    #image = tfImage.adjust_contrast(image,0.7)

    image = rgb2gray(image)


    #image = exposure.rescale_intensity(image)
    #image = enhance_contrast_percentile(image,disk(radius=3),p0=.1, p1=.9)
    #tr = threshold_local(image, 101, 'mean', offset=-(alt_thresh/255.0))
    tr = threshold_local(image, 101,'mean', mode= 'constant', cval=0, offset=-(alt_thresh / 255.0))
    
    #print("fiber is ", fiber)
    if fiber == 'dark':
        print("went")
        img_seg = (image >= tr).astype(uint8)
    else:
        print("light fibers")
        img_seg = (image < tr).astype(uint8)
    window_size = 25

    return img_seg

# def get_split_thresh_image(image,threshold):
#     image = rgb2gray(image)
#     img_grid,pore_grid,z_pore_grid = data_utils.split_up_image(image,num=3)
#     for i in range(len(img_grid)):
#         for j in range(len(img_grid[i])):
#             thresh = threshold * z_pore_grid[i][j]
#             img_seg = (image > threshold).astype(uint8)
#


def get_reg_thresh_image(image, threshold,fiber):
    #print(image)
    #image = gaussian(image,0.7)
    #image = tfImage.adjust_contrast(image,1.5)
    image = rgb2gray(image)
    if fiber == 'dark':
        #threshold = threshold_isodata(image,nbins=16,)
        #img_seg = (image > threshold).astype(uint8)
        img_seg = (image > threshold/255).astype(uint8)
        #img_seg = get_alt_thresh_image(img_seg, 30, fiber)
    else:
        img_seg = (image < threshold/255).astype(uint8)
    window_size = 25

    return img_seg
#
# def get_outline(img_seg):
#     x,y = img_seg.shape
#     #top edge
#     j =0
#     k = 0
#     print("ODD COL",)

def try_circle(coords, middle,size):
    go = True
    i = size
    area_pts = set()
    ls_x,ls_y = [],[]

    while go:
        ls_x,ls_y = disk((middle[0],middle[1]),i)
        j = 0
        circle_pts = {(ls_x[k],ls_y[k]) for k in range(1,len(ls_x))}
        pt = (0,0)
        if not coord_utils.check_circle(circle_pts,coords):
            go = False
        # while j < len(ls_x) and go:
        #     if go:
        #         pt = (ls_x[j],ls_y[j])
        #         if(coord_utils.check_pt(pt, middle, area_pts, coords)):
        #             area_pts.add(pt)
        #         else:
        #             go = False
        #     j= j + 1
        i = i + 1
    return i-1,(middle[0],middle[1])

# def area_backup(regions,r,area):
#     extra_circ = []
#     for region in regions:
#         if region.area>area:
#             center, max = get_largest_circle_in_region(region.coords,r-1)
#             if max>r:
#                 print('found larger')


def get_largest_circle_in_region(coords,max = 1,centroid= None):
    """ calculates the largest circle that will fit in the
    retion defined by reg_tup
    Parameters:
        reg_tup(tuple): details about pore
    Returns:
        tup: (center,radius,points"""
    center = [0,0]
    reg_coords = coords
    n = 0
    coord_set = coords
    #coord_set = {(reg_coords[j][0],reg_coords[j][1]) for j in range(0,len(coords))}
    for pt in reg_coords:
        if centroid is not None:
            pt = (centroid[0], centroid[1])
            print("testing centroid:", pt, " first")
            centroid = None
        n, pts = try_circle(coord_set, pt, max)
        if (n > max):
            max = n
            max_pts = pts
            center = pt
    print("MAX:", max)
    return center,max,
#
# def get_largest_holes(largest_areas,regions):
#     print("start get largest holes")
#     largest_holes = []
#     largest_holes_areas =[]
#
#     for large_area in largest_areas:
#         mid,r,pts, = get_largest_circle_in_region(large_area,centroid=large_area.centeroid)
#         largest_holes.append([mid,r])
#         largest_holes_areas.append([mid,r,pts])
#     for hole in largest_holes_areas:
#         area_backup(regions,hole[1],len(hole[2]))
#     largest_holes = sorted(largest_holes, key=lambda tup: float(tup[1]), reverse=True)
#     largest_holes_areas = sorted(largest_holes_areas, key=lambda tup: float(tup[1]),reverse=True)
#     print("large_holes", largest_holes)
#     return largest_holes,largest_holes_areas


def validate_area(region):
    print("area: ", region["area"])
    print(" filled area: ", region["filled_area"])
    print("ratio :", float(region["area"])/float(region["filled_area"]))
    




