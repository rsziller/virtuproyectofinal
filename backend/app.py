from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from bson.objectid import ObjectId
from datetime import datetime
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB = os.getenv("MONGO_DB")

mongo_uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"

client = MongoClient(mongo_uri)

db = client[MONGO_DB]

users = db.users
students = db.students

# LOGIN

@app.route('/register', methods=['POST'])
def register():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    existing_user = users.find_one({
        "username": username
    })

    if existing_user:
        return jsonify({
            "message": "Usuario ya existe"
        }), 400

    hashed_password = generate_password_hash(password)

    users.insert_one({
        "username": username,
        "password": hashed_password
    })

    return jsonify({
        "message": "Usuario registrado"
    }), 201

@app.route('/login', methods=['POST'])
def login():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    user = users.find_one({
        "username": username
    })

    if not user:
        return jsonify({
            "message": "Usuario no encontrado"
        }), 404

    if check_password_hash(user["password"], password):

        return jsonify({
            "message": "Login exitoso"
        }), 200

    return jsonify({
        "message": "Contraseña incorrecta"
    }), 401

# CRUD STUDENTS

@app.route('/students', methods=['GET'])
def get_students():

    data = []

    for student in students.find():

        data.append({
            "id": str(student["_id"]),
            "name": student["name"],
            "email": student["email"],
            "age": student["age"],
            "english_level": student["english_level"],
            "created_at": student["created_at"]
        })

    return jsonify(data)

@app.route('/students', methods=['POST'])
def create_student():

    data = request.json

    student = {
        "name": data["name"],
        "email": data["email"],
        "age": data["age"],
        "english_level": data["english_level"],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    students.insert_one(student)

    return jsonify({
        "message": "Estudiante creado"
    })

@app.route('/students/<id>', methods=['PUT'])
def update_student(id):

    data = request.json

    students.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "name": data["name"],
                "email": data["email"],
                "age": data["age"],
                "english_level": data["english_level"]
            }
        }
    )

    return jsonify({
        "message": "Estudiante actualizado"
    })

@app.route('/students/<id>', methods=['DELETE'])
def delete_student(id):

    students.delete_one({
        "_id": ObjectId(id)
    })

    return jsonify({
        "message": "Estudiante eliminado"
    })

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000
    )