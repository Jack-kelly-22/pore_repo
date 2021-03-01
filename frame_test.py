from utils import default_settings
from dtypes.Spreadsheets import Spreadsheet
from dtypes.job import Job
from dtypes.db_helper import Db_helper
from utils.input_utils import *
from utils.default_settings import *
import yappi
import os
db_helper = Db_helper()
options = default_settings.get_default_options()

yappi.set_clock_type("cpu") # Use set_clock_type("wall") for wall time
yappi.start()


options['job_name'] = 'diversity'
const = get_default_constants()
const = update_constants(const,120,"dark",200,70,False,55,True,5)
const["crop"] = True
const["boarder"] = 60
const['num_circles'] = 60
const['use_alt'] = False
const['adjust'] = True
options['constants'] = const

options["frame_paths"].append("./frames_folder/diversity-training")

job = Job(options,db_helper)
for folder in job.frame_ls[:1]:
    print("STARTING CREATE SPREADSHEET")
    Spreadsheet(folder,job.job_name)

yappi.get_func_stats().print_all()
yappi.get_thread_stats().print_all()
