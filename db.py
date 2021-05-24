from pymongo import MongoClient
from bson import ObjectId
from werkzeug.security import generate_password_hash
from datetime import datetime
from user import User

client = MongoClient("mongodb+srv://gokulsarath05:gokulsarath05@chat-room-app.k3gne.mongodb.net/Loan-Management-System-DB?retryWrites=true&w=majority")

chat_database = client.get_database('Loan-Management-System-DB')
users_collection = chat_database.get_collection('users')


def save_user(first_name, last_name, email, password, has_permission=False):
    password_hash = generate_password_hash(password)
    added_date_time = datetime.now().strftime("%d-%b-%Y, %H:%M:%S")
    group_id = users_collection.insert_one({'_id': email, 'first_name': first_name.capitalize(),
                                            'last_name': last_name.capitalize(), 'password': password_hash,
                                            'added_date_time': added_date_time,
                                            'has_permission': has_permission}).inserted_id
    return group_id

def get_user(email):
    user_data = users_collection.find_one({'_id': email})
    return User(user_data['_id'], user_data['first_name'],
                user_data['last_name'], user_data['password'],
                user_data['has_permission']) if user_data else None

def get_registered_users():
    return list(users_collection.find())

# save_user('admin', 'admin', 'admin@gmail.com', 'admin123', True)
# save_user('agent', 'agent', 'agent@gmail.com', 'agent123', True)
# email: admin@gmail.com
# password: admin123
