from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, \
                        current_user
from . import main
from .forms import LoginForm, RegistrationForm
from manage import app

with app.app_context(): #TODO: ugly, another way?
    from ..models import User

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/projects')
def projects():
    return render_template('projects.html')

@main.route('/notes')
def notes():
    return render_template('notes.html')

@main.route('/tags')
def tags():
    return render_template('tags.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        if User.verify_password(email, password):
            user = User(email=email)
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
        else:
            flash('Email or password is incorrect!', category='danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('main.index'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        if User.is_username_existed(username):
            flash('Username has existed', category='warning')
            return render_template('register.html', form=form)
        email = form.email.data
        if User.is_email_existed(email):
            flash('Email has exited', category='warning')
            return render_template('register.html', form=form)
        password = form.password.data
        User.add(username=username, email=email, password=password)
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)




