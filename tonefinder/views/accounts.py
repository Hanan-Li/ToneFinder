"""tonefinder file for accounts."""

import os
import flask
import MySQLdb
import MySQLdb.cursors
import tonefinder

# -------------------------------------------------------------------------------


@tonefinder.app.route('/accounts/login/', methods=['GET', 'POST'])
def login():
    """login."""
    if flask.request.method == 'POST':
        # Get database to check if user exists and password matches
        conn = tonefinder.model.get_db()
        cursor = conn.cursor()
        print(flask.request.form['username'])
        pass_word = cursor.execute(
            """SELECT * FROM users WHERE username = %s;""", 
            (flask.request.form['username'],))
        input_password = cursor.fetchone()
        if input_password is not None:
            input_password = input_password['password']
            pass_list = input_password.split('$')
            pass_word = tonefinder.views.util.pseudosha(
                pass_list[0],
                pass_list[1],
                flask.request.form['password']
                )
            if input_password is not None and pass_word == input_password:
                flask.session['username'] = flask.request.form['username']
                return flask.redirect(flask.url_for('show_index'))
            # If exists, add to cookies, redirect to index page.
    return flask.render_template('login.html')


@tonefinder.app.route('/accounts/signup/', methods=['GET', 'POST'])
def signup():
    """signup."""
    if flask.request.method == 'POST':
        # Get database to check if user exists and password matches
        if flask.request.form['password'] == '':
            flask.abort(400)
        if flask.request.form['password'] != flask.request.form['password2']:
            flask.abort(400)
        conn = tonefinder.model.get_db()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM users;""")
        usernames = cursor.fetchall()
        username = flask.request.form['username']
        res = next((sub for sub in usernames if sub['username'] == username), None)
        if res is None:
            password = tonefinder.views.util.sha512(flask.request.form['password'])
            cursor.execute("""INSERT `users` (`username`, `password`) VALUES (%s, %s)""",(username, password))
            conn.commit()
            flask.session['username'] = flask.request.form['username']
            return flask.redirect(flask.url_for('show_index'))
        else:
            flask.abort(409)
    return flask.render_template('signup.html')
# # -------------------------------------------------------------------------------


@tonefinder.app.route('/accounts/logout/')
def logout():
    """logout."""
    flask.session.clear()
    return flask.redirect(flask.url_for('login'))

# # -------------------------------------------------------------------------------


