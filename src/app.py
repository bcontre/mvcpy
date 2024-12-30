from flask import Flask, render_template, request, redirect, url_for, flash
from database import db
from controllers.UserController import UserController

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'  # Necesario para usar flash
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/users', methods=['POST'])
def create_user():
    return UserController.create_user()

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return UserController.get_user(user_id)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return UserController.delete_user(user_id)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return UserController.update_user(user_id, username, password)
    return UserController.edit_user(user_id)

@app.route('/users', methods=['GET'])
def list_users():
    return UserController.list_users()

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return UserController.register_user(username, password)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return UserController.login_user(username, password)
    return render_template('login.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form['user_input']
    return f'Has enviado: {user_input}'

if __name__ == '__main__':
    app.run(debug=True)