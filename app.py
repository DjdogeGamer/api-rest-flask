#from crypt import methods
import email
from unicodedata import name
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json
import sqlalchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/database'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))

    def to_json(self):
        return{"id": self.id, "name": self.name, "email": self.email}

@app.route("/users", methods=["GET"])
def select_users():
    users_objs = User.query.all()
    users_json = [user.to_json for user in users_objs]
    
    return generate_response(200, "users", users_json)

@app.route("/user/<id>", methods=["GET"])
def select_user(id):
    user_obj = User.query.filter_by(id=id).first()
    user_json = user_obj.to_json()

    return generate_response(200, "user", user_json)

def generate_response(status, content_name, content, message=False):
    body = {}
    body[content_name] = content

    if(message):
        body["message"] = message

    return Response(json.dumps(body), status=status, mimetype="application/json")

@app.route("/user", methods=["POST"])
def create_user():
    body = request.get_json()

    try:
        user = User(name=body["name"], email=body["email"])
        db.session.add(user)
        db.session.commit()
        return generate_response(201, "user", user.to_json(), "Created successfully")
    except Exception as e:
        print(e)
        return generate_response(400, "user", {}, "Error during registration")

@app.route("/user/<id>", methods=["PUT"])
def update_user(id):
    user_obj = User.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if("nome" in body):
            user_obj.name = body["name"]
        if("email" in body):
            user_obj.email = body["email"]

        db.session.add(user_obj)
        db.session.commit()
        return generate_response(201,"user", user_obj.to_json(), "Updated successfully")
    except Exception as e:
        print("Erro", e)
        return generate_response(400, "user", {}, "Error during update")

@app.route("/user/<id>", methods=["DELETE"])
def delete_user(id):
    user_obj = User.query.filter_by(id=id).first()

    try:
        db.session.delete(user_obj)
        db.session.commit()
        return generate_response(200, "user", user_obj.to_json(), "Deletion successfully")
    except Exception("Erro", e):
        return generate_response(400, "user", {}, "Error during deletion")

app.run()