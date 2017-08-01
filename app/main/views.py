from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, \
                        current_user
from . import main
from .forms import LoginForm, RegistrationForm, NoteForm
from manage import app

with app.app_context(): #TODO: ugly, another way?
    from ..models import User, Note, Tag

@main.route('/')
def index():
    return redirect(url_for('main.notes_index', start_index=0))

@main.route('/archive')
def archive():
    notes = Note.get_all_notes()
    return render_template('archive.html', notes=notes)

@main.route('/notes')
def notes():
    return redirect(url_for('main.notes_index', start_index=0))

@main.route('/notes/<int:start_index>')
def notes_index(start_index):
    notes = Note.get_notes(start_index)
    return render_template('notes.html', notes=notes)

@main.route('/tags')
def tags():
    tags = Tag.get_all_tags()
    return render_template('tags.html', tags=tags)

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

@main.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    form = NoteForm()
    if form.validate_on_submit():
        title = form.title.data
        tags = form.tags.data.replace(" ", "").strip(',').split(',')
        content = form.content.data
        author = current_user.username
        index = Note.add(title=title, tags=tags, content=content, author=author)
        return redirect(url_for('main.note', index=index))
    return render_template('write.html', form=form)

@main.route('/edit/<int:index>', methods=['GET', 'POST'])
@login_required
def edit(index):
    note = Note(index)

    if not note:
        abort(403)

    form = NoteForm()
    if form.validate_on_submit():
        title = form.title.data
        tags = form.tags.data.replace(" ", "").strip(',').split(',')
        content = form.content.data
        note.update(title=title, content=content, tags=tags)
        flash('Edit Saved.', category='success')
        return redirect(url_for('main.note', index=note.index))
    form.title.data = note.title
    tags_str = ','.join(note.tags)
    if tags_str:
        form.tags.data = tags_str
    form.content.data = note.content
    return render_template('edit.html', form=form, index=note.index)

@main.route('/note/<int:index>')
def note(index):
    note = Note(index)
    if note:
        return render_template('note.html', note=note)
    return redirect(url_for('main.index'))



