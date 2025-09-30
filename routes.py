from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session

from models import db, User, Product, Category, Cart, Order

from app import app
def auth_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return inner

@app.route('/')
@auth_required
def index():
    user = User.query.get(session['user_id'])
    if user.is_admin:
        return redirect(url_for('admin'))
    else:
        return render_template('index.html', user=User.query.get(session['user_id']))
    
@app.route('/admin')
@auth_required
def admin():
    user = User.query.get(session['user_id'])
    if not user.is_admin:
        flash('Access denied.')
        return redirect(url_for('index'))
    return render_template('admin.html', user=user, categories=Category.query.all())

@app.route('/profile')
@auth_required
def profile():
    return render_template('profile.html', user=User.query.get(session['user_id']))

@app.route('/profile', methods=['POST'])
@auth_required
def profile_post():
    user = User.query.get(session['user_id'])
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')
    cpassword = request.form.get('cpassword')
    if username == '' or name == '' or password == '' or cpassword == '':
        flash('Username and password are required.')
        return redirect(url_for('profile'))
    if not user.check_password(cpassword):
        flash('Incorrect current password.')
        return redirect(url_for('profile'))
    if User.query.filter(User.username==username, User.id!=user.id).first():
        flash('Username already taken. Please choose another.')
        return redirect(url_for('profile'))
    user.username = username
    user.name = name
    user.password = password
    db.session.commit()
    flash('Profile updated successfully.')
    return redirect(url_for('profile'))

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
    # login successful
    session['user_id'] = user.id
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

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/cart')
@auth_required
def cart():
    return ""

@app.route('/orders')
@auth_required
def orders():
    return ""

@app.route('/category/add')
@auth_required
def add_category():
    return render_template('category/add.html', user=User.query.get(session['user_id']))

@app.route('/category/add', methods=['POST'])
@auth_required
def add_category_post():
    name = request.form.get('name')
    if name == '':
        flash('Category name is required.')
        return redirect(url_for('add_category'))
    if len(name) > 64:
        flash('Category name is too long (max 64 characters).')
        return redirect(url_for('add_category'))
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    flash('Category added successfully.')
    return redirect(url_for('admin'))

@app.route('/category/<int:id>/show')
@auth_required
def show_category(id):
    return ""

@app.route('/category/<int:id>/edit')
@auth_required
def edit_category(id):
    return ""

@app.route('/category/<int:id>/delete')
@auth_required
def delete_category(id):
    return render_template('category/delete.html', user=User.query.get(session['user_id']), category=Category.query.get(id))

@app.route('/category/<int:id>/delete', methods=['POST'])
@auth_required
def delete_category_post(id):
    category = Category.query.get(id)
    if not category:
        flash('Category does not exist.')
        return redirect(url_for('admin'))
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully.')
    return redirect(url_for('admin'))