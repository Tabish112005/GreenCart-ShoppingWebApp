from flask import Flask, render_template, request, redirect, url_for, flash

from models import db, User, Product, Category, Cart, Order

from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == '' or password == '':
        flash('Username and password are required.')
        return redirect(url_for('login'))
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User does not exist.')
        return redirect(url_for('login'))
    if not user.check_password(password):
        flash('Incorrect password.')
        return redirect(url_for('login'))
    return redirect(url_for('index'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')
    if username == '' or password == '':
        flash('Username and password are required.')
        return redirect(url_for('register'))
    if User.query.filter_by(username=username).first():
        flash('Username already taken. Please choose another.')
        return redirect(url_for('register'))
    user = User(username=username, name=name, password=password)
    db.session.add(user)
    db.session.commit()
    flash('Registration successful. Please log in.')
    return redirect(url_for('login'))

