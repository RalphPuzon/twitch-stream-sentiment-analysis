import os, re, json, ast, csv
from datetime import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandasql import sqldf
from textblob import TextBlob
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

def jsonl_processor(file, csvpath):
	null = ''
	true = True
	false = False
	filename = file[:-5] + ".csv"
	with open(file) as f:
		for line in f:
			data_dict = json.dumps(line)
			data_dict = ast.literal_eval(data_dict)
			data_dict = eval(data_dict)

			date = dt.fromtimestamp(data_dict['timestamp']//1000).strftime("%Y-%m-%d")
			time = dt.fromtimestamp(data_dict['timestamp']//1000).strftime("%H:%M:%S")
			message = data_dict['message']
			
			with open(os.path.join(csvpath, filename), 'a+', newline="") as fl:
				writer = csv.writer(fl, delimiter = ',')
				fl.seek(0)
				if  fl.readline() == "":
					writer.writerow(['time', 'message'])
					writer.writerow([time, message])
				else:
					fl.seek(0,2)
					writer.writerow([time, message])

def grapher(file):
	#clean:
	df = pd.read_csv(file)
	df['message'] = df.message.apply(lambda x: x.lower())
	df['message'] = df.message.apply(lambda x: re.sub(r'[^A-Za-z0-9 ]+', '', x))
	df['message'] = df.message.apply(lambda x: x.split(' '))
	df['message'] = df.message.apply(lambda x: ' '. join([word for word in x if word not in stop_words]))
	df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.time
	#sentiment:
	df['sentiment'] = df.message.apply(lambda x: TextBlob(x).sentiment[0])

	#aggregate:
	q =   """SELECT time, 
					AVG(sentiment) as avg_sentiment
					FROM df 
					GROUP BY time"""

	chart_df = sqldf(q, locals())
	#graph
	curr_chart= sns.lineplot(x='time', 
				y='avg_sentiment', 
				data = chart_df)
	curr_chart.figure.savefig(file[:-4] + "_chart.png")
	curr_chart.clear()

if __name__ == "__main__":
	rec_root = os.path.join(os.path.realpath(__file__), '..', 'records')
	dirnames = os.listdir(rec_root)
	for direc in dirnames: #remember that the direc is also the channel name
		path = os.path.join(rec_root, direc)
		os.chdir(path)
		wfile = max([d for d in os.listdir('.') if d[-4:] == 'json'], key=os.path.getctime)
		jsonl_processor(wfile, path)
		gfile = max([d for d in os.listdir('.') if d[-3:] == 'csv'], key=os.path.getctime)
		grapher(gfile)
		
"""
this will be ran as a cron job everyday on the latest file.

convert epoch x to datetime in pst:
conv_dtime = datetime.fromtimestamp(x, tz=timezone('UTC'))
"""



    