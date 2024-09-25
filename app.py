from flask import Flask, jsonify, request
import sqlite3
import random
from faker import Faker
from data_dict import random_users

app = Flask(__name__)

# Create database connection and cursor
def get_db_connection():
    conn = sqlite3.connect('/Users/BirkLauritzen/Documents/KEA/3. semester/kode_fra_undervisning_e24/flask1/data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create table and drop it if it exists
with get_db_connection() as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS members (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        first_name TEXT, 
                        last_name TEXT, 
                        birth_date TEXT, 
                        gender TEXT, 
                        email TEXT, 
                        phonenumber TEXT, 
                        address TEXT, 
                        nationality TEXT,
                        active INTEGER, 
                        github_username TEXT)''')

    # Insert the random_users list into the database using executemany
    member_data = [(user['first_name'], user['last_name'], user['birth_date'], user['gender'], user['email'], 
                    user['phonenumber'], user['address'], user['nationality'], user['active'], user['github_username']) 
                   for user in random_users]

    conn.executemany('''INSERT INTO members (first_name, last_name, birth_date, gender, email, phonenumber, 
                        address, nationality, active, github_username) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', member_data)
    
    conn.execute('''UPDATE members SET github_username = "hej" WHERE id = 2''')
    
    conn.commit()

# GET - Read all members
@app.route('/members', methods=['GET'])
def read_all():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM members')
    members = cur.fetchall()
    conn.close()
    return jsonify([dict(member) for member in members])

# POST - Create a new member
@app.route('/members', methods=['POST'])
def create():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''INSERT INTO members (first_name, last_name, birth_date, gender, email, phonenumber, 
                address, nationality, active, github_username) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                (data['first_name'], data['last_name'], data['birth_date'], data['gender'], data['email'], 
                 data['phonenumber'], data['address'], data['nationality'], data['active'], data['github_username']))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Member added'}), 201

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)