"""
Tonefinder profiles (main) view.

URLs include:
/
"""

import os
import shutil
from operator import itemgetter
import arrow
import flask
import tonefinder
import matchering as mg


# -------------------------------------------------------------------------------


@tonefinder.app.route('/guitar', methods=['GET', 'POST'])
def show_guitar():
    """Display / route."""
    final_dict = {}
    if 'username' in flask.session:
        # Get the username
        user = flask.session['username']
        final_dict['username'] = user
        final_dict['login'] = True
        if flask.request.method == 'POST':
            print(flask.request.form)
            src_filename =  tonefinder.views.util.save_guitar_file()
            print(src_filename)
            target_dir = os.path.join(tonefinder.app.config['GUITAR_FOLDER'], user)
            if not os.path.isdir(target_dir):
                os.mkdir(target_dir)
            target_file = flask.request.form['guitar_name'] + '.wav'
            target_path = os.path.join(target_dir, target_file)
            print(target_path)
            shutil.copyfile(src_filename, target_path)
            conn = tonefinder.model.get_db()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO `guitar` (`name`, `guitarfile`, `owner`) VALUES (%s, %s, %s)""", 
                (flask.request.form['guitar_name'], target_file, user))
            conn.commit()
        return flask.render_template("guitar.html", **final_dict)
    else:
        return flask.redirect(flask.url_for('login'))



# -------------------------------------------------------------------------------

@tonefinder.app.route('/ir', methods=['GET'])
def show_ir():
    final_dict = {}
    if 'username' in flask.session:
        # Get the username
        user = flask.session['username']
        final_dict['username'] = user
        final_dict['login'] = True
        # if flask.request.method == 'POST':
        #     PASS

        return flask.render_template("ir.html", **final_dict)
    else:
        return flask.redirect(flask.url_for('login'))

# -------------------------------------------------------------------------------

@tonefinder.app.route('/guitar/<filename>', methods=['GET', 'POST'])
def get_guitar(filename):
    username = flask.session['username']
    conn = tonefinder.model.get_db()
    filename = filename[:-4]
    cursor = conn.cursor()
    cursor.execute(
        """SELECT guitarfile FROM guitar WHERE owner=%s AND name=%s;""",
        (username, filename))
    guitar_profile = cursor.fetchone()
    print(guitar_profile)
    guitarfile = guitar_profile["guitarfile"]
    print(guitarfile)
    directory = os.path.join(tonefinder.app.config['GUITAR_FOLDER'], username)
    print(directory)
    return flask.send_from_directory(directory,
                                     guitarfile)