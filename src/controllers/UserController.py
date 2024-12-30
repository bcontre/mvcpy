from flask import jsonify, redirect, url_for, render_template, request, flash
from models.models import User
from database import db
from sqlalchemy.exc import IntegrityError

class UserController:
    @staticmethod
    def create_user():
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('El nombre de usuario ya existe. Por favor, elige otro.', 'error')
            return redirect(url_for('register'))
        return redirect(url_for('list_users'))

    @staticmethod
    def get_user(user_id):
        user = User.query.get(user_id)
        if user:
            return jsonify({"user_id": user.id, "username": user.username})
        return jsonify({"message": "User not found"}), 404

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('list_users'))
        return jsonify({"message": "User not found"}), 404

    @staticmethod
    def edit_user(user_id):
        user = User.query.get(user_id)
        if user:
            return render_template('edit_user.html', user=user)
        return jsonify({"message": "User not found"}), 404

    @staticmethod
    def update_user(user_id, username, password):
        user = User.query.get(user_id)
        if user:
            user.username = username
            user.password = password
            db.session.commit()
            return redirect(url_for('list_users'))
        return jsonify({"message": "User not found"}), 404

    @staticmethod
    def list_users():
        users = User.query.all()
        return render_template('users.html', users=users)

    @staticmethod
    def register_user(username, password):
        new_user = User(username=username, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('El nombre de usuario ya existe. Por favor, elige otro.', 'error')
            return redirect(url_for('register'))
        return redirect(url_for('login'))

    @staticmethod
    def login_user(username, password):
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return redirect(url_for('hello_world'))
        return jsonify({"message": "Invalid credentials"}), 401