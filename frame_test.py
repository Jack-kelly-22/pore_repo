from utils import default_settings
from dtypes.Spreadsheets import Spreadsheet
from dtypes.job import Job
from dtypes.db_helper import Db_helper
from utils.input_utils import *
from utils.default_settings import *
import os
db_helper = Db_helper()
options = default_settings.get_default_options()

options['job_name'] = 'spread-tester'
const = get_default_constants()
print("path in frame_test",os.listdir())
const = update_constants(const,130,"dark",2000,20,False,55, False,50)
const['num_circles'] = 20
options['constants'] = const

options["frame_paths"].append("./frames_folder/single_black")

job = Job(options,db_helper)
for folder in job.frame_ls[:1]:
    print("STARTING CREATE SPREADSHEET")
    Spreadsheet(folder,job.job_name)

