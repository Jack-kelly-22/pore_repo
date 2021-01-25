from numpy import save as save
from numpy import load as load
from numpy import ndarray
from sqlite3 import Binary
import sqlite3
from io import BytesIO
import pickle

def fix_path(path):
        #return path.replace(" ","")
        #return path[1:]
        return path

def adapt_array(arr):
        out = BytesIO()
        save(out,arr)
        out.seek(0)
        return Binary(out.read())

def convert_array(text):
        out = BytesIO(text)
        out.seek(0)
        return load(out,allow_pickle=True)


def print_frame(cur):
        for row in cur:
                s = "frame_id:" + str(row[0]) 
                s = s +"frame_name:" + str(row[1])
                s = s +"frame_path:" + str(row[2])
                s = s +"frame_type:" + str(row[3])
                s = s +"tags:" + str(row[4])
                s = s +"avg_pore:" + str(row[6])
                # for image in row[5]:
                #         print_image(image)




def get_frame_fetch_str():
        s = ''' SELECT * from frames_index
                WHERE frame_id IN (SELECT frame_id 
                FROM frames_index
                WHERE frame_id = ?);'''
        return s

def get_img_fetch_str():
        s = ''' SELECT * from image_output
                WHERE img_id IN (SELECT img_id 
                FROM image_output
                WHERE img_id = ?);'''
        return s

def get_job_fetch_str():
        s = ''' SELECT * from jobs_index
                WHERE job_id IN (SELECT job_id 
                FROM jobs_index
                WHERE job_id = ?);'''
        return s

def get_img_post_str():
        s = ''' insert into image_output(img_id,img_name,img_path,pores,areas,all_areas,largest_holes,heat_img_path)
                           VALUES(?,?,?,?,?,?,?,?)'''
        return s

def get_jobs_fetch_str():
        s = '''SELECT * from jobs_index'''
        return s

"""def get_frame_post_str():

def get_job_post_str():"""


def list_jobs():
        conn = sqlite3.connect("/Users/jackkelly/jkdev/dash_vs/local/pore.db") 
        cur = conn.execute(''' SELECT job_id, job_name from jobs_index''')
        for row in cur:
                print("id:", row[0], type(row[0]))
                print("name:", row[1])
        print("done selecting")


def empty_job_dic():
        j_dat = {
                "job_id": None,
                "job_name": None,
                "job_path": None,
                "job_type": None,
                "tags": [],
                "frame_data_ls": []
        }
        return j_dat


def empty_frame_dic():
        f_dat = {
                "frame_id": "EMPTY_ID",
                "frame_name": "EMPTY_NAME",
                "frame_path": "EMPTY_PATH",
                "frame_type": "EMPTY_TYPE",
                "frame_date": "EMPTY_DATE",
                "tags": ["EMPTY_TAGS"],
                "image_data_ls": [],
                "avg_pore": 0,
                "thresh": 0,
                "scale": 0,
                "frame_largest_ls": [],
                "frame_options": {},
                "hist": [],
                "hist_bins":[],
                "hist_area_img_path":'',
                "hist_diam_img_path":'',
                "disk_area_img_path" : '',
                "disk_pore_img_path":''
        }
        return f_dat


def empty_img_dic():
        im_dat = {
                "img_id": None,
                "img_name": None,
                "img_path": None,
                "pores": None,
                "img_largest_areas": [],
                "all_areas": None,
                "largest_holes": [],
                "heat_img_path":""
        }
        return im_dat