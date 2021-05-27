from pymongo import MongoClient
from bson import ObjectId
from werkzeug.security import generate_password_hash
from datetime import datetime
from user import User
from plan import Plan
from type import Type

client = MongoClient("mongodb+srv://gokulsarath05:gokulsarath05@chat-room-app.k3gne.mongodb.net/Loan-Management-System-DB?retryWrites=true&w=majority")

lms_database = client.get_database('Loan-Management-System-DB')
users_collection = lms_database.get_collection('users')
loan_plans_collection = lms_database.get_collection('loan_plans')
loan_types_collection = lms_database.get_collection('loan_types')

# =============================== User Related ===============================

def save_user(first_name, last_name, email, password, has_permission=False):
    password_hash = generate_password_hash(password)
    added_date_time = datetime.now().strftime("%d-%b-%Y, %H:%M:%S")
    users_collection.insert_one({'_id': email, 'first_name': first_name.capitalize(),
                                            'last_name': last_name.capitalize(), 'password': password_hash,
                                            'added_date_time': added_date_time,
                                            'has_permission': has_permission}).inserted_id


def get_user(email):
    user_data = users_collection.find_one({'_id': email})
    return User(user_data['_id'], user_data['first_name'],
                user_data['last_name'], user_data['password'],
                user_data['has_permission']) if user_data else None


def get_registered_users():
    return list(users_collection.find())


def delete_user(email):
    users_collection.delete_one({'_id': email})


def update_user(first_name, last_name, email, password, has_permission=False):
    password_hash = generate_password_hash(password)
    added_date_time = datetime.now().strftime("%d-%b-%Y, %H:%M:%S")
    users_collection.update_one({'_id': email}, {'$set': {'first_name': first_name.capitalize(),
                                 'last_name': last_name.capitalize(), 'password': password_hash,
                                 'added_date_time': added_date_time, 'has_permission': has_permission}})


# =============================== Loan Plan Related ===============================

def save_loan_plan(months, years, interest, penalty):
    loan_plans_collection.insert_one({'months': months, 'years': years, 'interest': interest, 'penalty': penalty})


def get_a_loan_plan(id):
    loan_plan_data = loan_plans_collection.find_one({'_id': ObjectId(id)})
    return Plan(loan_plan_data['_id'], loan_plan_data['years'],
                loan_plan_data['months'], loan_plan_data['interest'],
                loan_plan_data['penalty']) if loan_plan_data else None


def get_all_loan_plans():
    return list(loan_plans_collection.find())


def delete_a_loan_plan(id):
    loan_plans_collection.delete_one({'_id': ObjectId(id)})


# =============================== Loan Type Related ===============================

def save_loan_type(type, description):
    loan_types_collection.insert_one({'type': type, 'description': description})


def get_a_loan_type(id):
    loan_type_data = loan_types_collection.find_one({'_id': ObjectId(id)})
    return Type(loan_type_data['_id'], loan_type_data['type'],
                loan_type_data['description']) if loan_type_data else None


def get_all_loan_types():
    return list(loan_types_collection.find())


def delete_a_loan_type(id):
    loan_types_collection.delete_one({'_id': ObjectId(id)})


# save_user('admin', 'admin', 'admin@gmail.com', 'admin123', True)
# save_user('agent', 'agent', 'agent@gmail.com', 'agent123', True)
# email: admin@gmail.com
# password: admin123
