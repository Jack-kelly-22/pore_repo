from dtypes.imageData import ImageData
import time
from utils import data_utils
from os import mkdir
import sqlite3
from utils.sql_utils import adapt_array,convert_array
from numpy import ndarray,array
from utils.data_utils import *
import uuid
import os
import shutil
from matplotlib import pyplot as plt
from numpy import std
from math import pi
class Frame:

    def get_images_in_path(self,path):
        imgs = os.listdir(path)
        imgs_paths = []
        for img in imgs:
            if(img[0]!="."):
                imgs_paths.append(path + "/" +img)
        return imgs_paths


    def __init__(self,path,out,inspect_mode,constants,db_ref,jname,tags):
        """
        name: what to call the frame
        image_ls: list of images paths
        inspect_mode: light/dark
        """
        self.name = os.path.basename(os.path.normpath(path))

        self.job_name = jname
        self.image_paths = self.get_images_in_path(path)
        self.tags = tags
        self.type = inspect_mode
        self.out_path = out
        self.id = str(uuid.uuid4()).replace('-','') + "_" + self.name
        self.constants = constants
        self.image_data_ls = []
        self.image_ref_ls = []
        self.avg_pore = 0
        self.all_areas = []
        self.histogram = []
        self.hist_bins = []
        self.largest_holes = []
        self.largest_areas = []
        self.heat_img_path = ''
        self.area_hist_path,self.diam_hist_path,self.area_pie_path,self.pore_pie_path = '','','',''
        self.area_std,self.diam_std = 0,0
        self.db_ref = db_ref
        self.create_dir()
        self.process_frame()
        self.save_histograms()
        #self.save_pie()
        #self.save_pie_pores()
        #self.save_heat_img()
        #self.heat_intensity_path = get_intensity_heatmap()
        self.add_frame_db()

    # def save_heat_img(self):
    #     #pore_ls1 = [image.porosity for image in self.image_data_ls[:len(self.image_data_ls)//2]]
    #     #pore_ls2 = [image.porosity for image in self.image_data_ls[len(self.image_data_ls)//2:]]
    #     #if len(pore_ls2)
    #     #pore_ls = [pore_ls1,pore_ls2]
    #     pore_ls = [[image.porosity for image in self.image_data_ls]]
    #     name_ls = [[image.name[:-4] for image in self.image_data_ls]]
    #     self.heat_img_path = data_utils.get_diff_heatmap(self.name,None,np.array(pore_ls),self.out_path + self.job_name+"/",name_ls)
    def create_dir(self):
        try:
            mkdir("./job-data/" + self.job_name + '/' + self.name)
        except Exception as e:
            print('frame exist... NUKE...',"./job-data/" + self.job_name + '/' + self.name)
            print("with exception:", e)
            shutil.rmtree("./job-data/" + self.job_name + '/' + self.name)
            os.makedirs("./job-data/" + self.job_name + '/' + self.name)

    def save_histograms(self):
        self.save_histogram_hole_diameter()
        self.save_histogram_hole_area()

    def add_frame_db(self):
        sqlite3.register_adapter(ndarray, adapt_array)
        sqlite3.register_converter("array", convert_array)
        conn = sqlite3.connect(
            "dash_app/data/pore.db",
            detect_types=sqlite3.PARSE_DECLTYPES)
        out_path = "./job-data/" +self.job_name + '/' +self.name
        sql_str = ''' insert into frames_index(
        frame_id,
        frame_name,
        frame_path,
        frame_type,
        tags,
        image_data_ls,
        avg_pore,threshold,
        scale_v,
        hist,
        hist_bins,
        hist_area_img_path,
        hist_diam_img_path,
        disk_area_img_path,
        disk_pore_img_path,
        heat_img_path)
                        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        type = 0
        if self.type == 'light':
            type = 1

        if self.constants['use_alt']:
            thresh = self.constants['alt_thresh']
        else:
            thresh = self.constants['thresh']
        conn.execute(sql_str,(self.id,
                              self.name,
                              out_path,
                              int(type),
                              str(self.tags),
                              array(self.image_ref_ls),
                              float(self.avg_pore),
                              int(thresh),
                              str(self.constants["scale"]),
                              array(self.histogram),
                              array(self.hist_bins),
                              self.area_hist_path,
                              self.diam_hist_path,
                              self.area_pie_path,
                              self.pore_pie_path,
                              self.heat_img_path
                              ))
        conn.commit()
        conn.close()
        print("image data pushed to database")
    def process_frame(self):
        """ creates instances ImageData objects for all 
        images and adds them so self.image_data_ls
        """
        i =0
        for img in self.image_paths:
            self.process_image(img)
            i = i + 1
        self.histogram,self.hist_bins = get_histogram(self.all_areas,self.constants['scale'],self.constants['min_ignore'])
        self.avg_pore = str(self.avg_pore/len(self.image_data_ls))
            

    def process_image(self,img):
        """ creates new ImageData objects and appends"""
        print("starting image processing of file with path:",img)
        new_image = ImageData(
            jname=self.job_name,
            frame = self.name,
            path = img,
            const = self.constants, 
            db_ref = self.db_ref,
            )
        self.image_data_ls.append(new_image)
        self.image_ref_ls.append(new_image.im_id)
        self.all_areas = self.all_areas + new_image.all_areas
        self.largest_holes = self.largest_holes + new_image.largest_holes
        self.largest_areas = self.largest_areas + new_image.largest_areas
        self.avg_pore = self.avg_pore + new_image.porosity

    def save_histogram_hole_diameter(self):
        #print(self.largest_holes)
        largest_diams = [x[1]*2*float(self.constants["scale"]) for x in self.largest_holes]
        self.diam_std = std(largest_diams)
        print("STD diam:", self.diam_std)
        plt.hist(largest_diams,10)
        plt.xlabel("Diameter(microns)")
        plt.ylabel("Frequency")
        plt.title("Histogram of Diameter of top " + str(len(largest_diams)) + " Largest Circles")
        plt.savefig("./job-data/" + self.job_name + '/' + self.name + '/' + "diameter_histogram.png")
        self.diam_hist_path = "./job-data/" + self.job_name + '/' + self.name + '/' + "diameter_histogram.png"


    def save_histogram_hole_area(self):
        #print(self.largest_holes)
        plt.clf()
        largest_areas = [(x[1]**2) * pi * (float(self.constants["scale"])**2) for x in self.largest_holes]
        plt.hist(largest_areas,bins = 10)
        self.area_std = std(largest_areas)
        print("STD area:", self.area_std)
        plt.xlabel("Area(microns^2)")
        plt.ylabel("Frequency")
        plt.title("Histogram of Area of Top " + str(len(largest_areas)) + " Largest Circles")
        plt.savefig("./job-data/" + self.job_name + '/' + self.name + '/' + "area_histogram.png")
        self.area_hist_path = "./job-data/" + self.job_name + '/' + self.name + '/' + "area_histogram.png"


    def compute_fractions(self):
        lables = [image.name for image in self.image_data_ls]
        area_totals = [0] * len(self.image_data_ls)
        area_totals = {image.name:0 for image in self.image_data_ls}
        area_sum = 0
        for area in self.largest_holes:
            area_totals[area[2]] = area_totals[area[2]] + area[1]
            area_sum = area[1]
        for k,v in area_totals.items():
            area_totals[k] = v/area_sum
        print("THIS is AREA TOTALS",area_totals)
        return area_totals

    def save_pie(self):
        area_dic = self.compute_fractions()
        labels = area_dic.keys()
        plt.clf()
        plt.title("Portion of Largest Areas by image")
        plt.text()
        plt.pie(area_dic.values(),labels=area_dic.keys(),
               autopct='%1.1f%%',
               shadow=True,
               startangle=90
        )
        plt.axis('equal')
        plt.savefig("./job-data/" + self.job_name + '/' + self.name + '/' + "area_pie_chart.png")
        self.area_pie_path = "./job-data/" + self.job_name + '/' + self.name + '/' + "area_pie_chart.png"

    #
    # def save_pie_pores(self):
    #     print("creating pore pie chart")
    #     names = [image.name for image in self.image_data_ls]
    #     vals = [image.porosity*100 for image in self.image_data_ls]
    #
    #     plt.clf()
    #     plt.title("Share of Porosity by Image")
    #     plt.pie(vals, labels= names,
    #             autopct='%1.1f%%',
    #             shadow=True,
    #             startangle=90
    #     )
    #     self.pore_pie_path = "./job-data/" + self.job_name + '/' + self.name + '/' + "pore_pie_chart.png"
    #     plt.savefig(self.pore_pie_path)


    
