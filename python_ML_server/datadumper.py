import os
from sklearn.externals import joblib
import json
import datetime

dump_file_path = 'data/clf_data.pkl'
metadata_file_path = 'data/data.json'

# checks whether the path exist or else it will create the file
def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

# dump trained clasifier to path $dump_file_path
def dump_ml(clf):
	
	ensure_dir(dump_file_path)
	joblib.dump(clf, dump_file_path) 


#retrive data from dumped file location $dump_file_path
def get_ml():
	try:
 		clf = joblib.load(dump_file_path)
 		return clf
 		# break
	except Exception as e:
 		print  e
 		return None

def dump_metadata(data):
	with open(metadata_file_path, 'w') as outfile:
		json.dump(data, outfile)


def get_metadata():
	try:
		with open(metadata_file_path) as data_file:    
    			data = json.load(data_file)
 			return data
 		# break
	except Exception as e:
 		print  e
 		return None

data = {}
data['time'] = 'Aug 10 2016  3:00PM'
json_data = json.dumps(data)

dump_metadata(json_data)

abc = get_metadata()

print json.loads(abc)['time']


print datetime.datetime.now()