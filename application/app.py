
from os import urandom,getenv 
import sys
import json
from flask import Flask,render_template, request,redirect,url_for,make_response
from flask.json import JSONEncoder
from pymongo import MongoClient,errors
from bson.objectid import ObjectId
from flask import Flask, session
from flask_session import Session





# create a Flask app
app = Flask(__name__)
app.secret_key = urandom(24) # a string of 24 random bytes
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


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
host_url = str(getenv("HOST_URL"))

class DB_int():
    @staticmethod
    def db_int():
        try:
            
            print("Attempting to connect to database server....")
            print("Authentication parameters: ",{"MONGODB_HOST ": mongoHost,"MONGODB_AUTH_USER ":mongoUsername,"MONGODB_AUTH_PWD" : mongoPassword,"MONGODB_DATABASE": mongoDB}) 

            client = MongoClient(mongoHost,username=mongoUsername,password=mongoPassword,authSource=mongoDB)
            
            print("[+] Database connected!")
        
        except errors.ServerSelectionTimeoutError as e: 
            print('Could not connect to MongoDB: {}'.format(e))
            
        db = client[mongoDB]

        return db

db = DB_int().db_int()


@app.route("/auth",methods=['GET', 'POST'])
def auth():
    user_name = request.get_json().get('username', '')
    password = request.get_json().get('password', '')
    users = db.users.find({"username": user_name}, {"_id": 0}).limit(1)
    users = list(users)
    if len(users) > 0 and password == users[0]["password"]:
        session["user"] = {"username":user_name,"id" :users[0]["string"]}       
        return {"url":host_url,"id":users[0]["string"]}        
    else:
        return make_response({"error": "Invalid Credentials. Please log in again."}), 400
            
    


@app.route("/login")
def login():
    return render_template("login.html")



@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))


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
    name = request.get_json().get('name', '')
    tel = request.get_json().get('number', '')
    uniq_id = request.get_json().get('_id', '')
    my_query = {"_id": ObjectId(uniq_id)}
    db.people.find_one_and_update(my_query, {"$set": {'name': name,'number': tel}})
    return {"msg":"Updated"}

    

@app.route("/remove_person", methods=['POST'])
def remove(): 
    uniq_id = request.get_json().get("id","")
    my_query = {"_id":ObjectId(uniq_id)}
    if my_query:   
        db.people.find_one_and_delete(my_query)
        return {"msg":"Deleted"}
    return "Entity Not Found!"


@app.route("/")
def index():
    if not session.get("user") and request.endpoint != 'login':
        return redirect(url_for('login'))

    return render_template("index.html")



app.threaded = True
app.use_reloader = app.debug = False


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=int(eval(getenv("HOST_PORT"))))