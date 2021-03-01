from skimage.segmentation import chan_vese
from numpy import percentile,histogram,linalg,copy
import cv2
import time
import matplotlib.pyplot as plt
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
from skimage.morphology import binary_opening,area_opening
from skimage.exposure import equalize_adapthist
from skimage.filters import threshold_sauvola,threshold_local,threshold_otsu
#from skimage.filters.rank import enhance_contrast_percentile
#from PIL import ImageEnhance
import numpy as np

import random

import matplotlib.pyplot as plt
import skimage
from skimage import restoration
#from skimage.transform import rescale

from sklearn.feature_extraction import image as img2
from sklearn.cluster import spectral_clustering
from sklearn.utils.fixes import parse_version

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
    largest_pores = []
    ig = float(image_data.ignore_size)
    regions = [region for region in regions if region.area>ig]
    print("#OF REGIONS: ",len(regions))

    #regions = sorted(regions,key = lambda tup: t)
    regions.sort(key=lambda reg:reg["area"],reverse=True)
    # regions.reverse()
    largest_circles = []
    i = 0
    import time
    timer = time.perf_counter()
    min_area = 0
    min_r = 1
    incl_coords = set()

    #largest_circles = get_largest_circles(regions,image_data.constants['num_circles'])
    largest_circles = get_largest_holes(regions, image_data, image_data.constants)

    for region in regions[:100]:
        if region['area']>min_area:
            y, x, = region["centroid"]
            coords = region["coords"]
            x,y=int(x),int(y)
            coords = coord_utils.remove_z_set(coords)
            incl_coords=incl_coords.union(coords)

            temp_coords = coords
            largest_pores.append(
                [image_data.name,
                 int(region.area * (image_data.scale_factor * image_data.scale_factor)),
                 (x // 1),
                 (y // 1),
                 region["centroid"],
                 1
                 ])
            #print("reg:" + str(i) + '/' + str(len(regions)) )
            i = i + 1
        else:
            print("hit min area")


    largest_pores.sort(key=lambda p: p[1], reverse=True)

    largest_circles.sort(key= lambda x: x[1],reverse=True)
    print("time for area and circle calc:", time.perf_counter() - timer)
    return largest_pores,regions,largest_circles


def get_largest_holes(regions,image_data,constants):
    holes = []

    min = 0
    if(len(regions) < constants['num_circles']*2):
        n = len(regions)-1
    else:
        n = constants['num_circles'] * 2
    i=0
    for region in regions[:n]:
        #find the largest hole in reg
        y, x, = region["centroid"]
        coords = region["coords"]
        coords = coord_utils.remove_z_set(coords)
        x, y = int(x), int(y)
        #coords = coord_utils.remove_z_set(coords)
        center, r = get_largest_circle_in_region(coords, max=int(region['minor_axis_length'] * 0.2),
                                              centroid=(int(x), int(y)))
        center =(center[0],center[1])
        holes.append([center, r, image_data.name,i])
        i+=1
    holes.sort(key=lambda x:x[1],reverse=True)
    holes=holes[:constants['num_circles']]
    min = holes[-1][1]**2*31.4
    for hole in holes[:constants['num_circles']]:
        if(min<len(regions[hole[3]]['coords'])):
            center,r,reg_coords = hole[0],hole[1],regions[hole[3]]['coords']
            # print("reg-coords",type(reg_coords),reg_coords)
            circle_coords = disk(center, radius=r)
            coord_set = {(reg_coords[j][0], reg_coords[j][1]) for j in range(0, len(reg_coords))}
            coords = coord_utils.remove_z_set(reg_coords)
            # print("len:",len(reg_coords))
            circle_coords = {(circle_coords[0][j],circle_coords[1][j]) for j in range(0,len(circle_coords[0]))}
            area_coords=[]
            while(len(circle_coords)<0.5 * len(coords)):
                #checking for secondary circle
                # print("looking for third")
                area_coords = coords - circle_coords
                center, r = get_largest_circle_in_region(area_coords,)
                center = (center[0], center[1])
                holes.append([center,r,image_data.name])
                cir = disk(center, radius=r)
                circle_coords = circle_coords.union(set({(cir[0][j], cir[1][j]) for j in range(0, len(cir[0]))}))
                #print('circle coords:',len(circle_coords))
    return holes



def get_largest_areas_simple(regions, constants):

    largest_pores = []
    ig = float(constants['ignore_size'])

    regions = [region for region in regions if region.area > ig]
    regions.sort(key=lambda reg: reg["area"], reverse=True)
    largest_circles = []
    i = 0
    for region in regions:
        y, x, = region["centroid"]
        coords = region["coords"]
        coords = coord_utils.remove_z_set(coords)
        center, r = get_largest_circle_in_region(coords, centroid=(int(x), int(y)))
        largest_circles.append([center, r, 'subImage'])


        center = (center[0], center[1])
        largest_pores.append(
            ["subImage",
             int(region.area * (constants['scale_factor'] **2)),
             (x // 1),
             (y // 1),
             center,
             r
             ])
        i = i + 1
    largest_circles.sort(key=lambda x: x[1], reverse=True)
    largest_pores.sort(key=lambda x: x[1], reverse=True)

    return largest_pores, regions, largest_circles

def sum_images(colored,original,boarder):
    r_cons, g_cons, b_cons = [0, 0, 0]
    r_, g_, b_ = colored[:, :, 0], colored[:, :, 1], colored[:, :, 2]
    rb = np.pad(array=r_, pad_width=boarder // 2, mode='constant', constant_values=r_cons)
    gb = np.pad(array=g_, pad_width=boarder // 2, mode='constant', constant_values=g_cons)
    bb = np.pad(array=b_, pad_width=boarder // 2, mode='constant', constant_values=b_cons)
    padded = np.dstack(tup=(rb, gb, bb))

    return np.where(padded!=0,padded,original)


def get_crop_image(image,boarder):
    y,x,z = image.shape
    bx,by = 800-boarder,600-boarder
    startx = x // 2 - (bx // 2)
    starty = y // 2 - (by // 2)
    cropped = image[starty:starty + by, startx:startx + bx]
    return cropped


def get_thresh_image(image, constants):
    if constants["use_alt"]:
        print("USED ALT THRESH")
        img_seg = get_alt_thresh_image(image, constants["alt_thresh"],constants['fiber_type'])
    else:
        #image = rgb2gray(image)
        print("start regular thresh")
        img_seg = get_reg_thresh_image(image, constants["thresh"],constants['fiber_type'])
    return img_seg



def get_alt_thresh_image(image,alt_thresh,fiber,):
    image = rgb2gray(image)

    tr = threshold_local(image, 601,'mean', mode= 'constant', cval=0, offset=-(alt_thresh / 255.0))
    
    #print("fiber is ", fiber)
    if fiber == 'dark':
        print("went")
        img_seg = (image >= tr).astype(uint8)
    else:
        print("light fibers")
        img_seg = (image < tr).astype(uint8)

    window_size = 25
    return img_seg



def get_reg_thresh_image(image, threshold,fiber):
    # image = equalize_adapthist(image, clip_limit=0.02)
    #image = tfImage.adjust_contrast(image,1.5)
    image = rgb2gray(image)



    if fiber == 'dark':
        img_seg = (image > threshold/255).astype(uint8)
    else:
        img_seg = (image < threshold/255).astype(uint8)
    window_size = 25

    return img_seg

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
        i = i + 1
    return i-1,(middle[0],middle[1])




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
    i = max
    #coord_set = {(reg_coords[j][0],reg_coords[j][1]) for j in range(0,len(coords))}
    for pt in reg_coords:
        if centroid is not None:
            pt = (centroid[0], centroid[1])
            #print("testing centroid:", pt, " first")
            centroid = None
            center=pt
        n, pts = try_circle(coord_set, pt, max)
        if (n > max):
            max = n
            max_pts = pts
            center = pt

    print("found max-:", max)
    return center,max,
#
#


def validate_area(region):
    print("area: ", region["area"])
    print(" filled area: ", region["filled_area"])
    print("ratio :", float(region["area"])/float(region["filled_area"]))
    




