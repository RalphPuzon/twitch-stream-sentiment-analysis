import os, glob, re, json, ast, csv
from datetime import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandasql import sqldf
from textblob import TextBlob
pysqldf = lambda q: sqldf(q, globals())

def jsonl_processor(file, csvpath):
	with open('file') as f:
		for line in f:
			data_dict = eval(ast.literal_eval(json.dumps(line)))
			date = dt.fromtimestamp(data_dict['timestamp']//1000).strftime("%Y-%m-%d")
			time = dt.fromtimestamp(data_dict['timestamp']//1000).strftime("%H:%M:%S")
			channel = data_dict['channel'][1:]
			message = data_dict['message']
			filename = file[:-5] + ".csv"

			with open(os.path.join(csvpath, channel, filename), 'a+', newline="") as fl:
				writer = csv.writer(fl, delimiter = ',')
				fl.seek(0)
				if  f.readline() == "":
					writer.writerow(['time', 'message'])
					writer.writerow([time, message])
				else:
					f.seek(0,2)
					writer.writerow([time, message])

def grapher(file, csvpath, channel):
	pass
	#TODO: 	process csv for textblob, generate sentiment, aggregate by time, generate graph




			
if __name__ == "__main__":
	rec_root = os.path.join(os.path.realpath(__file__), '../records')
	dirnames = os.listdir(rec_root)
	for direc in dirnames:
		path = rec_root + direc
		os.chdir(path)
		wfile = max(os.listdir('./'), key=os.path.getctime)
		jsonl_processor(wfile, path)
		gfile = max(os.listdir('./'), key=os.path.getctime)
		grapher(gfile, path, direc)
		

"""
this will be ran as a cron job everyday on the latest file.

P O A:
- for every folder: check for the latest json file
  store original path, cd into that folder
- we have a json lines text format file as input
- parse each line, gather needed data and write to csv
	basic approach:
		
		import json

		data = []
		with open('file') as f:
		    for line in f:
		        data.append(json.loads(line))
		

	* clean data as needed as well
- add csv sentiment column
- write out csv
- if write out is robust:
	delete json
- perform sql aggregation to time and sentiment cols
- generate graph.
  

convert epoch x to datetime in pst:
conv_dtime = datetime.fromtimestamp(x, tz=timezone('UTC'))
"""



    