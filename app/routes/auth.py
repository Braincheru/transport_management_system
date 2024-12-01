from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

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
