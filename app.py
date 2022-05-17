# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sqlite3

import markdown
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import app

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdasdfhhawreujyhtgrfewlhguehfieshfuwilugulrhioejpwJJ'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@app.route('/create/', methods=('GET', 'POST'))
def create():
    conn = get_db_connection()
    if request.method == 'POST':
        content = request.form['content']
        if not content:
            flash('Content is required!')
            return redirect(url_for('index'))
        conn.execute('INSERT INTO posts (content) VALUES (?)', (content,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        content = request.form['content']

        if not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET content = ?'
                         ' WHERE id = ?',
                         (content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format("Post # " + str(post['id'])))
    return redirect(url_for('index'))


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    post['content'] = markdown.markdown(post['content'])
    return render_template('post.html', post=post)


@app.route('/')
def index():
    conn = get_db_connection()
    db_posts = conn.execute('SELECT * FROM posts').fetchall()
    print(db_posts)
    conn.close()

    posts = []

    for post in db_posts:
        post = dict(post)
        post['content'] = markdown.markdown(post['content'])
        posts.append(post)
    return render_template('index.html', posts=posts)

@app.route('/about/')
def about():
    return render_template('about.html')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    index()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
