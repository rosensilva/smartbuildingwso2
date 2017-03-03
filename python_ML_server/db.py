#!/usr/bin/python

import MySQLdb
import datetime

host_name = "localhost"
user_address = "root"
user_passwd = "qwe123"
database_name = "headCount_DB"


def roundTime(tm=None, roundTo=30):
  dt  = tm
  tm = tm - datetime.timedelta(minutes=tm.minute % roundTo,
                             seconds=tm.second,
                             microseconds=tm.microsecond)
  if tm == dt :
  	tm = tm - datetime.timedelta(minutes = 30)
  return tm




def getDataBetweenTimeInterval(startTime,endTime,floor):
	results = []
	time = roundTime(startTime)
	db = MySQLdb.connect (host = host_name,
    	                          user = user_address,
        	                      passwd = user_passwd,
            	                  db = database_name)

	# prepare a cursor object using cursor() method
	cursor = db.cursor()
	while(time<endTime):

		sql = "SELECT * FROM dailycount WHERE Floor = '" +floor+ "' AND Date = '"+ time.strftime("%Y-%m-%d")+"' AND time = '"+time.strftime("%H:%M")+"'"       
		time = time + datetime.timedelta(minutes = 30)
		cursor.execute(sql)
   	
   		# Fetch one row in a list of lists.
		sqlResults = cursor.fetchone()
		if cursor.rowcount == 0 :
			print "Error in Database ! No Data Recieved..."
			break
		results.append(sqlResults[1])


	# disconnect from server
	db.close()

	return results


def getWindowData(initialTime, windowSize, isTraining, floor):
	
	#for traing window we need traingWindow and real value to train datamodel

	if isTraining :
		windowSize = windowSize + 1
	results = []
	time = roundTime(initialTime)
	time = time - datetime.timedelta(minutes = 30*windowSize)
	

	db = MySQLdb.connect (host = host_name,
    	                          user = user_address,
        	                      passwd = user_passwd,
            	                  db = database_name)



	# prepare a cursor object using cursor() method
	cursor = db.cursor()
	for i in range(0,windowSize):
		

		sql = "SELECT * FROM dailycount WHERE Floor = '" +floor+ "' AND Date = '"+ time.strftime("%Y-%m-%d")+"' AND time = '"+time.strftime("%H:%M")+"'"       
		time = time + datetime.timedelta(minutes = 30)
		cursor.execute(sql)
   	
   		# Fetch all the rows in a list of lists.
		sqlResults = cursor.fetchone()
		if cursor.rowcount == 0 :
			print "No Data!"
			db.close()
			return None
		results.append(sqlResults[1])


	# disconnect from server
	db.close()

	return results


def getOccupancy(inTime , floor):
	
	time = roundTime(inTime)
	db = MySQLdb.connect (host = host_name,
    	                          user = user_address,
        	                      passwd = user_passwd,
            	                  db = database_name)
	cursor = db.cursor()

	sql = "SELECT * FROM dailycount WHERE Floor = '" +floor+ "' AND Date = '"+ time.strftime("%Y-%m-%d")+"' AND time = '"+time.strftime("%H:%M")+"'"

	cursor.execute(sql)

	sqlResults = cursor.fetchone()
		
	if cursor.rowcount == 0 :
		print "No Data!"
		db.close()
		return None

	else:
		db.close()
		return sqlResults 




