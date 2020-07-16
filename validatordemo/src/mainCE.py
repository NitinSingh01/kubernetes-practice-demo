import pymysql
import mysql.connector
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
	
	db_connection = mysql.connector.connect(
	host="35.194.34.57",
	user="sa",
	passwd="password",
	database="UID"
	)
	my_database = db_connection.cursor()
	sql_statement = "SELECT * FROM UID"
	my_database.execute(sql_statement)
	output = my_database.fetchall()
	resp = jsonify(output)
	return resp
		
@app.route('/users', methods=['POST'])
def add_user():
	_json = request.json
	_firstname = _json['FirstName']
	_lastname = _json['LastName']
	_uid = _json['UID']
	sql = "INSERT INTO UID(UID, FirstName, LastName) VALUES(%s, %s, %s)"
	data = (_uid, _firstname, _lastname)
	db_connection = mysql.connector.connect(
	host="35.194.34.57",
	user="sa",
	passwd="password",
	database="UID"
	)
	conn = db_connection.cursor(pymysql.cursors.DictCursor)
	conn.execute(sql, data)
	db_connection.commit()
	return "Record Inserted"
	
@app.route('/validate', methods=['POST'])
def validate_user():
	_json = request.json
	_firstname = _json['FirstName']
	_lastname = _json['LastName']
	_uid = _json['UID']
	db_connection = mysql.connector.connect(
	host="35.194.34.57",
	user="sa",
	passwd="password",
	database="UID"
	)
	conn = db_connection.cursor(pymysql.cursors.DictCursor)
	sql = "SELECT * FROM UID WHERE UID=%s And FirstName=%s And LastName=%s"
	data = (_uid,_firstname,_lastname)
	conn.execute(sql,data)
	row = conn.fetchone()
	if row is None:
		return "UID not found. Please try again !"
	else: 
		return "Validation Successful"
	
		
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE)