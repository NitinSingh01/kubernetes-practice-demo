from pymongo import MongoClient
from flask import jsonify
from bson.json_util import dumps
from flask import Flask, request

import config

app = Flask(__name__)

@app.route("/Hello")
def hello():
	print("Hi")
	return "Hello World!"		

		
@app.route('/users',methods=['GET'])
def users():
	
	client = MongoClient('mongodb')
	db = client.UID
	col = db.UID
	Output = dumps(col.find())
	return Output
		
@app.route('/users', methods=['POST'])
def add_user():
	_json = request.json
	_firstname = _json['FirstName']
	_lastname = _json['LastName']
	_middlename = _json['MiddleName']
	_uid = _json['UID']
	if _uid and _firstname and _lastname and _middlename:
		client = MongoClient('mongodb')
		db = client.UID
		col = db.UID
		data = {"FirstName":_firstname,"LastName":_lastname,"UID":_uid,"MiddleName":_middlename}
		col.insert(data)
		return "Record Inserted"
	else:
		return "Required field/fields is/are missing"
	

@app.route('/validate', methods=['POST'])
def validate_user():
	_json = request.json
	_uid = _json['UID']
	_firstname = _json['FirstName']
	_lastname = _json['LastName']
	if _uid and _firstname and _lastname:
		client = MongoClient('mongodb')
		db = client.UID
		col = db.UID
		output=dumps(col.find_one({"UID": _uid,"FirstName":_firstname,"LastName":_lastname}))
		if output is None:
			return "Invaild UID. Please try again."
		else:
			return "Validation successful"
	else: 
		return "Please enter UID"
		
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE)