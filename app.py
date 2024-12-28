import re
from flask import Flask, flash, redirect,render_template, request, jsonify, session, url_for
import json
import mysql.connector
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from src.models.User import User

app = Flask(__name__)

app.secret_key = 'iloveyou'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Enter your database connection details below
db_config = {
    'user': 'user',
    'password' : 'user',
    'host': '127.0.0.1',
    'database': 'Library'
}
@login_manager.user_loader
def load_user(uname):
    try:
        # Kết nối đến cơ sở dữ liệu
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Truy vấn để lấy thông tin người dùng
        cursor.execute("SELECT * FROM TaiKhoan WHERE uname = %s", (uname,))
        user_data = cursor.fetchone()

        if user_data:
            return User(user_data['uname'])  # Giả sử User có constructor nhận id và username
        else:
            return None  # Không tìm thấy người dùng
    except mysql.connector.Error as err:
        print(f"Error: {str(err)}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
@app.route('/test')
def test():
    try:
        #Connect to the db
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        #Query the db
        cursor.execute("SELECT * FROM Sach")
        results = cursor.fetchall()
        return jsonify(results)
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}),500
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

@app.route('/', methods=['GET'])
def default():
    return render_template('login.html')

@app.route('/home', methods=['GET'])
@login_required
def home():
    return render_template('user/home.html', username = current_user.id)

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()# Get JSON data from request
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'success': False, 'message': 'Missing username or password'}), 400
        
        # Check credentials
        try:
            #Connect to the db
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor(dictionary=True)

            #Query the db
            cursor.execute("SELECT * FROM TaiKhoan WHERE uname = %s AND password = %s", (username, password))
            account = cursor.fetchone()
            if account:
                #Create session data, we can access this data in other routes
                session['logged_in'] = True
                session['username'] = account['uname']
                user = User(account['uname'])
                login_user(user)
                return jsonify({'success': True, 'message': 'Login successful', 'redirect': '/home'}), 200
            else:
                return jsonify({'success': False,'message': 'Invalid username or password'}), 401
                
        except mysql.connector.Error as err:
            return jsonify({'error': str(err)}), 500
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
            else:
                return jsonify({'success': False, 'message': 'Request must be JSON.'}), 400

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    return redirect(url_for('default'))

# Create API get data from database
@app.route("/api/books/community", methods=['GET'])
def get_books_community():
    try:
        #Connect to the db
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        #Query the db
        cursor.execute("SELECT * FROM Sach ORDER BY RAND() LIMIT 3")
        results = cursor.fetchall()
        return jsonify(results), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}),500
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

@app.route("/api/books/popular", methods=['GET'])
def get_books_popular():
    try:
        #Connect to the db
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        #Query the db
        cursor.execute("SELECT * FROM Sach ORDER BY RAND() LIMIT 5")
        results = cursor.fetchall()
        return jsonify(results), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}),500
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

@app.route("/api/books/recentAdd", methods=['GET'])
def get_books_recentAdd():
    try:
        #Connect to the db
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        #Query the db
        cursor.execute("SELECT * FROM Sach ORDER BY RAND() LIMIT 3")
        results = cursor.fetchall()
        return jsonify(results), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}),500
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == '__main__':
    app.run(debug=True)