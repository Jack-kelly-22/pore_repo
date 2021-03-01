from flask import Flask, jsonify,request
from flask_restful import Resource
from dtypes.job import Job
import json
import threading
from dtypes.db_helper import Db_helper
import os

#from dash_app.app import celery
from dtypes.Spreadsheets import Spreadsheet
class Queue(Resource):
    def __init__(self):
        self.queue = []
        self.db_helper = Db_helper()
        self.num_frames = 0
        self.num_images = 0
        self.process_queue()

    def get(self):
        return {'jobs':len(self.queue),
                'frames':self.num_frames}

    def post(self):
        options = request.get_json(force=True)
        print("Job added tqueue")
        #print(type(options),options)
        #print(type(json.loads(options)))
        #self.queue.append(options)

        return jsonify(self.queue)

    def process_queue(self):
        threading.Timer(5.0,self.process_queue).start()
        while len(self.queue)!=0:
            print("Starting queued job ")
            item = self.queue.pop()
            job = Job(item, self.db_helper)
            for folder in job.frame_ls:
                Spreadsheet(folder,job.job_name)


