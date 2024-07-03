from flask import Flask, request, render_template, redirect, url_for, session
import pymysql
from model.check_login import is_existed, exist_user, is_null
from model.check_regist import add_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于会话管理，确保安全性

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = pymysql.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to pymysql DB successful,", connection)
    except Exception as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        print("Query executed successfully, result:", records)
        return records
    except Exception as e:
        print(f"The error '{e}' occurred")
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
            print("pymysql connection is closed")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if is_null(username, password):
            login_message = "温馨提示：账号和密码是必填"
            return render_template('login.html', message=login_message)
        elif is_existed(username, password):
            session['username'] = username  # 设置会话
            return redirect(url_for('search'))
        elif exist_user(username):
            login_message = "温馨提示：密码错误，请输入正确密码"
            return render_template('login.html', message=login_message)
        else:
            login_message = "温馨提示：不存在该用户，请先注册"
            return render_template('login.html', message=login_message)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if is_null(username, password):
            register_message = "温馨提示：账号和密码是必填"
            return render_template('register.html', message=register_message)
        elif exist_user(username):
            register_message = "温馨提示：用户已存在，请直接登录"
            return render_template('register.html', message=register_message)
        else:
            add_user(username, password)
            return redirect(url_for('user_login'))
    return render_template('register.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'username' not in session:
        return redirect(url_for('user_login'))  # 未登录则重定向到登录页面
    
    if request.method == 'POST':
        search_query = request.form['search_query']
        conn = create_connection('120.46.3.93', 'root', '0411mtxM+', 'real_estae')
        if conn:
            query = f"SELECT * FROM real_estate_price WHERE 省会名称 = '{search_query}'"
            records = execute_query(conn, query)
            return render_template('result.html', records=records)
    return render_template('search.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
