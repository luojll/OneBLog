from flask import render_template, flash
from . import main

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