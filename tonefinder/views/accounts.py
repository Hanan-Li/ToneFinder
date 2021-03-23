"""Insta485 file for accounts."""

import os
import flask
import tonefinder

# -------------------------------------------------------------------------------


@insta485.app.route('/accounts/login/', methods=['GET', 'POST'])
def login():
    """login."""
    if flask.request.method == 'POST':
        # Get database to check if user exists and password matches
        conn = insta485.model.get_db()
        pass_word = conn.execute(
            "SELECT password FROM users WHERE username = ?;",
            (flask.request.form['username'],))
        input_password = pass_word.fetchone()
        if input_password is not None:
            input_password = input_password['password']
            pass_list = input_password.split('$')
            pass_word = insta485.views.util.pseudosha(
                pass_list[0],
                pass_list[1],
                flask.request.form['password']
                )
            if input_password is not None and pass_word == input_password:
                flask.session['username'] = flask.request.form['username']
                return flask.redirect(flask.url_for('show_index'))
            # If exists, add to cookies, redirect to index page.
    return flask.render_template('login.html')

# -------------------------------------------------------------------------------


@insta485.app.route('/accounts/logout/')
def logout():
    """logout."""
    flask.session.clear()
    return flask.redirect(flask.url_for('login'))

# -------------------------------------------------------------------------------


@insta485.app.route('/accounts/create/', methods=['GET', 'POST'])
def create():
    """create."""
    if flask.session.get('username') is not None:
        return flask.redirect(flask.url_for('login'))
    if flask.request.method == 'POST':
        if flask.request.form['password'] == '':
            flask.abort(400)
        conn = insta485.model.get_db()
        users = conn.execute('SELECT username FROM users;')
        usernames_old = users.fetchall()
        if any(a['username'] == flask.request.form['username']
               for a in usernames_old):
            flask.abort(409)
        # GET PROFILE PIC
        filename = insta485.views.util.get_file()
        pass_word = insta485.views.util.sha512(flask.request.form['password'])
        conn.execute('INSERT INTO \
                     users(username, fullname, email, filename, password)\
                     VALUES(?,?,?,?,?)',
                     (flask.request.form['username'],
                      flask.request.form['fullname'],
                      flask.request.form['email'],
                      filename,
                      pass_word))
        flask.session['username'] = flask.request.form['username']
        return flask.redirect(flask.url_for('show_index'))
    return flask.render_template('create.html')


@insta485.app.route('/accounts/edit/', methods=['GET', 'POST'])
def edit():
    """edit."""
    if 'username' in flask.session:
        logname = flask.session['username']
        if flask.request.method == 'POST':
            conn = insta485.model.get_db()
            if flask.request.files.get('file') is not None:
                filename = insta485.views.util.get_file()
                old = conn.execute("SELECT filename FROM users \
                                    WHERE username = ?;",
                                   (logname,))
                old_filename = old.fetchone()['filename']
                if old_filename != '':
                    old_file_path = os.path.join(
                        insta485.app.config["UPLOAD_FOLDER"],
                        old_filename
                    )
                    os.unlink(old_file_path)
                conn.execute("UPDATE users SET filename = ? WHERE username=?;",
                             (filename, logname))
            new_name = flask.request.form['fullname']
            email = flask.request.form['email']
            conn.execute("UPDATE users SET fullname = ?, \
                         email = ? WHERE username = ?;",
                         (new_name, email, logname))
        conn = insta485.model.get_db()
        use = conn.execute("SELECT * FROM users WHERE username=?;", (logname,))
        user = use.fetchone()
        return flask.render_template('edit.html', **user)
    return flask.redirect(flask.url_for('login'))


@insta485.app.route('/accounts/delete/', methods=['GET', 'POST'])
def delete():
    """delete."""
    if 'username' in flask.session:
        logname = flask.session['username']
        if flask.request.method == 'POST':
            conn = insta485.model.get_db()
            profile = conn.execute("SELECT filename FROM users \
                                    WHERE username = ?;",
                                   (logname,))
            pic = profile.fetchone()['filename']
            pic_path = os.path.join(
                insta485.app.config["UPLOAD_FOLDER"],
                pic
            )
            os.unlink(pic_path)
            pot = conn.execute("SELECT filename FROM posts WHERE owner=?;",
                               (logname,))
            posts = pot.fetchall()
            for post in posts:
                post_name = post['filename']
                post_path = os.path.join(
                    insta485.app.config["UPLOAD_FOLDER"],
                    post_name
                )
                os.unlink(post_path)
            conn.execute("DELETE FROM users WHERE username = ?;", (logname,))
            flask.session.clear()
            return flask.redirect(flask.url_for('create'))

        conn = insta485.model.get_db()
        use = conn.execute("SELECT * FROM users WHERE username=?;", (logname,))
        user = use.fetchone()
        return flask.render_template('delete.html', **user)
    return flask.redirect(flask.url_for('login'))


@insta485.app.route('/accounts/password/', methods=['GET', 'POST'])
def password():
    """password."""
    if 'username' in flask.session:
        logname = flask.session['username']
        conn = insta485.model.get_db()
        if flask.request.method == 'POST':
            old_p = flask.request.form['password']
            new_p = flask.request.form['new_password1']
            new_p_1 = flask.request.form['new_password2']
            db_p = conn.execute("SELECT password FROM users WHERE username=?;",
                                (logname,))
            db_password = db_p.fetchone()['password']
            db_list = db_password.split('$')
            old_p_hash = insta485.views.util.pseudosha(db_list[0],
                                                       db_list[1],
                                                       old_p)
            if old_p_hash != db_password:
                flask.abort(403)
            if new_p != new_p_1:
                flask.abort(401)

            hashed_new_p = insta485.views.util.sha512(new_p)
            conn.execute('UPDATE users SET password=? WHERE username=?;',
                         (hashed_new_p, logname))
            return flask.redirect(flask.url_for('edit'))
        return flask.render_template('password.html')
    return flask.redirect(flask.url_for('login'))
