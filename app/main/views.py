from flask import render_template, flash
from . import main
from manage import app

with app.app_context(): #TODO ugly, another way?
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

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/register')
def register():
    return render_template('register.html')