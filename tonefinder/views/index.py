"""
Tonefinder index (main) view.

URLs include:
/
"""

import os
from operator import itemgetter
import arrow
import flask
import tonefinder
import matchering as mg


# -------------------------------------------------------------------------------


@tonefinder.app.route('/', methods=['GET', 'POST'])
def show_index():
    """Display / route."""
    final_dict = {}
    if 'username' in flask.session:
        # Get the username
        user = flask.session['username']
        final_dict['login'] = True
        final_dict['username'] = user
        final_dict['submitted'] = False
        # Database portion
        if flask.request.method == 'POST':
            src_file, ref_file, input_src, input_ref = tonefinder.views.util.save_file()
            print(src_file)
            if src_file != "" and ref_file != "":
                target_file = input_src
                target_dir = os.path.join(tonefinder.app.config['TRANSFORMED_FOLDER'], user)
                if not os.path.isdir(target_dir):
                    os.mkdir(target_dir)
                target_path = os.path.join(target_dir, target_file)

                ir = input_src[:-4] + "_" + input_ref[:-4] + "_ir.wav"
                ir_dir = os.path.join(tonefinder.app.config['IR_FOLDER'], user)
                if not os.path.isdir(ir_dir):
                    os.mkdir(ir_dir)
                ir_path = os.path.join(ir_dir, ir)
                mg.process(
                    target=src_file,
                    reference=ref_file,
                    # pcm16 and pcm24 are just basic shortcuts
                    # You can also use the Result class to make some advanced results
                    results=[
                        mg.Result(
                            target_path, subtype="PCM_24", use_limiter=False
                        )
                    ],
                    ir_file = ir_path
                )
                final_dict['submitted'] = True
                final_dict['transformed'] = target_file
                final_dict['irfile'] = ir

        return flask.render_template("index.html", **final_dict)
    else:
        return flask.redirect(flask.url_for('login'))



# -------------------------------------------------------------------------------




@tonefinder.app.route('/ir_file/<filename>', methods=['GET'])
def get_ir(filename):
    username = flask.session['username']
    directory = os.path.join(tonefinder.app.config['IR_FOLDER'], username)
    return flask.send_from_directory(directory,
                                     filename)

@tonefinder.app.route('/transformed_file/<filename>', methods=['GET', 'POST'])
def get_transformed(filename):
    username = flask.session['username']
    directory = os.path.join(tonefinder.app.config['TRANSFORMED_FOLDER'], username)
    return flask.send_from_directory(directory,
                                     filename)
