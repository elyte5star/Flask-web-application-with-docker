
from os import urandom,getenv 
import sys
import json
from flask import Flask,render_template, request
from flask.json import JSONEncoder
from pymongo import MongoClient,errors
from bson.objectid import ObjectId





# create a Flask app
app = Flask(__name__)

app.secret_key = urandom(24) # a string of 24 random bytes
app.config["SESSION_TYPE"] = "filesystem"
#client = MongoClient('localhost', 27017)
#db = client.anzyz

class MyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(MyEncoder, self).default(obj)

app.json_encoder = MyEncoder

# global variables for MongoDB host
mongoHost = str(getenv("MONGODB_HOST"))
mongoPort = int(getenv("MONGODB_PORT"))
mongoDB = str(getenv("MONGODB_DATABASE"))
mongoUsername = str(getenv("MONGODB_AUTH_USER"))
mongoPassword = str(getenv("MONGODB_AUTH_PWD"))


class DB_int():
    @staticmethod
    def db_int():
        try:
            print("Trying to connect to database server!!")
            client = MongoClient(host = [ mongoHost + ":" + str(mongoPort) ],serverSelectionTimeoutMS = 3000,username = mongoUsername,password = mongoPassword)
            print ("server version:", client.server_info()["version"])
            print("Connected to database server!")
        except errors.ServerSelectionTimeoutError as e: 
            print('Could not connect to MongoDB: {}'.format(e))

        db = client[mongoDB]
        return db

db = DB_int().db_int()  

@app.route('/get_ppl', methods =['GET'])
def get_list_of_ppl():
    people_in_office = db.people.find({ })
    my_dict = {}
    if people_in_office:
        for x in people_in_office:
            aux = [x['name'], x['number']]
            my_dict[str(x["_id"])] = aux
        return {"data": my_dict} 
    return {"data": "empty"} 
    
@app.route('/add_person',methods = ["POST"])
def add_person():
    data = request.data
    name = request.get_json().get('name', '')
    tel = request.get_json().get('number', '')
    if data:
        db.people.insert_one({'name': name, 'number': tel} )
        print("Insert_one "+ name + " " + tel)
        return {"msg":"An entity added"}
    return {"msg":"Couldnt add an entity"}
      

@app.route('/update_entity', methods=["POST"])
def update_entity():
    data = request.data
    if data:
        name = request.get_json().get('name', '')
        tel = request.get_json().get('number', '')
        uniq_id = request.get_json().get('_id', '')
        my_query = {"_id": uniq_id}
        db.people.update_one(my_query, {"$set": {'name': name,'number': tel}})
        return {"msg":"Updated"}
    return " "
    

@app.route("/remove_person", methods=['POST'])
def remove(): 
    uniq_id = request.get_json().get("id","")
    my_query = {"_id": uniq_id}
    if my_query:
        db.people.delete_one(my_query)
        return {"msg":"Deleted"}
    return "Entity Not Found!"


@app.route("/")
def index(): 
    return render_template("index.html")


app.threaded = True
app.use_reloader = app.debug = False


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=int(eval(getenv("HOST_PORT"))))