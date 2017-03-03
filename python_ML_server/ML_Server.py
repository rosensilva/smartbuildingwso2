#!/usr/bin/python


import db as database
import datadumper as dumper
import threading
import time
import pandas as pd
import matplotlib.pylab as plt
import json
import seaborn as sns
import numpy as np
import datetime
import urlparse
import logging
import flask
import threading

from sklearn.metrics import mean_absolute_error
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
from sklearn.ensemble import RandomForestRegressor
from OpenSSL import SSL
from flask_cors import CORS, cross_origin
from flask import Flask, Response

# create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('ssl.key')
context.use_certificate_file('ssl.cert')

windowSize = 286

clf = RandomForestRegressor()

initialTime = datetime.datetime.strptime('Aug 8 2016  3:30PM', '%b %d %Y %I:%M%p')
endTime = datetime.datetime.strptime('Oct 8 2016  3:30PM', '%b %d %Y %I:%M%p')


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator



def importCsv(csvfile, header):
	data = pd.read_csv(csvfile)
	values = data[header].values.flatten()	
	
	return values
	
def getWindowedArray(timeSeries, windowSize):
	windows = []
	for i in range(windowSize, len(timeSeries)):
		windows.append(timeSeries[i-windowSize:i])
	return windows
	
def plotGraph(timeSeries, predictions):
	plt.plot( np.arange(len(predictions)), predictions, '--r',linewidth=2)
	plt.plot( np.arange(len(timeSeries)), timeSeries,'b',linewidth=1)
	plt.show()
		
def splitData(X, y, test_size):
	split_size = int(test_size*len(X))
	
	return X[split_size:], X[:split_size], y[split_size:], y[:split_size]

def predict(time):
	global windowSize
	window = getWindowedArray(initialTime = time, windowSize = windowSize , isTraining = False, floor = '1st Floor')
	return clf.predict(window)

def init():
	global initialTime
	global clf
	global windowSize
	global endTime


	currentTime = datetime.datetime.now()

	#//TODO : make python servers ml model a serializable one 

	# clf_d = dumper.get_ml()
	# if clf_d == None:
	# 	print "Didn't retrive clf data"
	# else:
	# 	clf = clf_d		


	# metadata = dumper.get_metadata()

	# if metadata == None:
	# 	print "Didn't retrive clf data"
	# else:
	# 	initialTime = datetime.datetime.strptime(json.loads(metadata)['time'], '%b %d %Y %I:%M%p')	



	trainingData = database.getDataBetweenTimeInterval(startTime = initialTime ,endTime =endTime,floor = '1st Floor')

	logger.info("Size of the recieved data from : "+ str(endTime - initialTime)+" is "+str(len(trainingData))) 

	X = getWindowedArray(trainingData,windowSize)
	y = trainingData[windowSize:]

	clf.fit(X, y)


def dataModelTrainer():
	global windowSize
	global clf

	time_string = '2016-10-10 13:00'
	inputTime = datetime.datetime.strptime(time_string, '%Y-%m-%d %H:%M')

	dataWindow = database.getWindowData(initialTime = inputTime, windowSize = windowSize, isTraining = True, floor= '1st Floor')

	
	clf.fit([dataWindow[:(windowSize-1)]],[dataWindow[-1]])

	logger.info("Trained data model for time :" + time_string + "with window " + str(dataWindow[:(windowSize-1)])+ " for real value of " + str([dataWindow[-1]]))
	


def traingThread():
  threading.Timer(60.0*30, traingThread).start()
  logger.info("Data Model Training thread is running")




#######################################
# Actual Server Code Starts from here # 	
#######################################


logger.info("Python Machine Learning Server Starting up...")
init()
#traingThread()
logger.info ("initialization Complete!")

app = Flask(__name__)



@app.route("/")
@crossdomain(origin='*')
def hello():
	return "Hello there, Python Machine Learning server is working!"


@app.route("/currentprediction", methods = ['GET'])
@crossdomain(origin='*')
def getCurrentPredicion():
	time_string = '2016-10-10 13:00'
	inputTime = datetime.datetime.strptime(time_string, '%Y-%m-%d %H:%M')
	dataWindow = database.getWindowData(initialTime = inputTime, windowSize = windowSize, isTraining = False, floor= '1st Floor')
	ans = clf.predict([dataWindow])
	resp = str(ans)
	
	resp = resp.replace("[ ","")
	resp = resp.replace("]","")
	return str(resp)


@app.route("/currentoccupancy", methods = ['GET'])
@crossdomain(origin='*')
def getCurrentOccupancy():
	time_string = '2016-10-10 13:01'
	inputTime = datetime.datetime.strptime(time_string, '%Y-%m-%d %H:%M')
	headCount = database.getOccupancy(inTime = inputTime , floor = '1st Floor')
	a = str(headCount)
	tokens = a.split(",")
	returnStr = tokens[1]
	returnStr = returnStr.replace("L","")
	return str(returnStr)


# @app.route('/getpredict', methods=['POST'])
# @crossdomain(origin='*')
# def getPrediction():
# 	global windowSize	

# 	print "this is the request:  "\
#logger.info(request.query_string)
# 	json_data = json.dumps(urlparse.parse_qs(request.query_string))
# 	time_string = json.loads(json_data)['date'][0] +" "+ json.loads(json_data)['time'][0]
# 	print time_string
# 	inputTime = datetime.datetime.strptime(time_string, '%Y-%m-%d %H:%M')

# 	logger.info("Fletching data from database for" + str(inputTime) )
# 	dataWindow = database.getWindowData(initialTime = inputTime, windowSize = windowSize, isTraining = False, floor= '1st Floor')
# 	ans = clf.predict([dataWindow])
# 	print "End of request"
# 	# return request.query_string
# 	logger.info("Predicted count "+ str(ans))

@app.route('/dastemp', methods=['POST'])
@crossdomain(origin='*')
def recieveTemp():
	print "request came"	
	return "done!" 
 
	

@app.errorhandler(404)
def page_not_found(error):
    return 404, 200



if __name__ == "__main__":
	app.run('192.168.1.101', 5000, app,
           ssl_context='adhoc')

