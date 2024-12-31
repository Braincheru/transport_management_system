from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__)

@bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Extract form data
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # Check for existing user
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another.', 'danger')
            return redirect(url_for('auth.sign_up'))

        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, role=role)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Profile created successfully! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating profile: {str(e)}', 'danger')

    return render_template('sign_up.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('driver.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', user=current_user)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'driver':
        return redirect(url_for('driver.dashboard'))
    elif current_user.role == 'officer':
        return redirect(url_for('officer.dashboard'))
    elif current_user.role == 'transport_officer':
        return redirect(url_for('transport_officer.dashboard'))
    return "Role not recognized", 400


