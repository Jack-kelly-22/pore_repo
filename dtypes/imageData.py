#import pandas as pd
from skimage.measure import label, regionprops
import cv2
from cv2 import resize
import uuid
from utils import image_utils, area_utils,data_utils
from dtypes.db_helper import Db_helper
from skimage import io
import os
import numpy as np
from dash_app.components import dash_reusable_components as drc
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt
import skimage
from skimage.transform import rescale #resize
class ImageData:
    def __init__(self,jname,frame,path,const, db_ref,dat = None):
        #create unique identifier for imagedata object in db
        self.im_id = str(uuid.uuid4()).replace('-','') + "_" + frame
        #this should be the root path for output of data/images
        self.constants = const
        print("DO I crop:",const['crop'],type(const['crop']))
        #this should strickty be the name of the image(no delimeters)
        self.name = os.path.basename(os.path.normpath(path))
        self.path = "/job-data/" + jname + "/" + frame
        self.image_out_path = "/job-data/" + jname + "/" + frame + '/' + self.name[:-4] + "_out" +'.png'
        self.image_out_path_og = "/job-data/" + jname + "/" + frame + '/' + self.name[:-4] + "_og"+'.png'
        self.img_seg = []
        self.heat_out_path = ''
        #opens the image and stores the image data `as a np array
        self.img_path = path
        #unique identifier for the image
        self.frame_id = frame
        #value that indicates the sensitytiy of the thresholding
        self.threshold = const["thresh"]
        #factor to convert the images size to microns
        self.scale_factor = float(const["scale"])
        #size of pore to alert on or show in red
        self.danger_size = const['warn_size']
        #pore size to ignore IMPORTANT
        self.ignore_size = const['min_ignore']
        self.regions = None
        self.num_circles = const['num_circles']
        self.img_grid =[]
        self.dat = dat
        #scale image
        self.image_handle = None
        self.filtered_image = None
        self.out_image = None
        self.porosity = 0
        self.largest_areas = []
        self.largest_regions = []
        self.largest_holes = None
        self.all_areas = []
        self.coords = []
        self.histogram = None
        self.heat_diff_out_path =''
        self.avg_pore = 0

        self.db_ref = db_ref
        self.compute_image(path,const)


    def compute_image(self,path,const):
        print("start compute...")
        max = 1
        max_pts = []
        pts = []
        orig = None
        if self.dat == None:
            image_data = io.imread(path)
        else:
            image_data = (drc.b64_to_numpy(self.dat, False))


        image=resize(image_data, dsize =(800,600), interpolation = cv2.INTER_AREA)
        image_utils.save_out_image(image,self.image_out_path_og)
        if 'x0' in const.keys():
            x0, y0 = int(const["x0"]), int(const["y0"])
            x1, y1 = int(const["x1"]), int(const["y1"])
            image[y0:y1, x0:x1]=(drc.b64_to_numpy(self.dat, False))
            print("Updating image")

        if const['crop']:
            orig = image
            image = area_utils.get_crop_image(image, const['boarder'])


        #image = area_utils.adjust_exposure(image)

        self.img_seg = area_utils.get_thresh_image(image,const)


        self.porosity = area_utils.get_porosity(self.img_seg)
        print("Porosity of ", self.name, " :", self.porosity)
        label_image = label(self.img_seg)
        regions = regionprops(label_image)
        self.regions = regions
        self.all_areas = area_utils.get_all_areas(regions)
        self.largest_areas, self.largest_regions, self.largest_holes = area_utils.get_largest_areas(regions, self)
        self.out_image = image_utils.color_out_image(regions, image, const["multi"],const['min_ignore'],const['scale'])
        self.out_image = image_utils.color_out_largest(self.largest_regions, self.out_image)
        self.out_image = image_utils.color_holes2(self.largest_holes[:const['num_circles']], self.out_image)

        if const['crop']:
            i=0
            while i<len(self.largest_holes):
                center = (self.largest_holes[i][0][0]+const['boarder'],self.largest_holes[i][0][1]+const['boarder'])
                self.largest_holes[i][0]=center
                i+=1
            self.out_image = area_utils.sum_images(self.out_image,orig,const['boarder'])
            self.out_image = image_utils.add_boarder(self.out_image,const['boarder'])

        image_utils.save_out_image(self.out_image, self.image_out_path)
        db = Db_helper()
        db.post_img_to_db(self)
