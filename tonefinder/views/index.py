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
        # Database portion
        if flask.request.method == 'POST':
            print(flask.request.files)
            src_file, ref_file = tonefinder.views.util.save_file()
            print("src file", src_file)
            print("ref file", ref_file)
            if src_file is not None and ref_file is not None:
                target_file = src_file[5:]
                print("target file", target_file)
                target_path = os.path.join(tonefinder.app.config['TRANSFORMED_FOLDER'], target_file)
                ir = src_file[5:-4] + "_" + ref_file[5:-4] + "_ir.wav"
                ir_path = os.path.join(tonefinder.app.config['IR_FOLDER'], ir)
                print(target_path)
                print(ir_path)
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


# @insta485.app.route('/uploads/<filename>')
# def get_image(filename):
#     """Get image."""
#     if not os.path.isfile(os.path.join(insta485.app.config['UPLOAD_FOLDER'],
#                                        filename)):
#         return flask.abort(404)
#     return flask.send_from_directory(insta485.app.config['UPLOAD_FOLDER'],
#                                      filename)

@tonefinder.app.route('/ir_file/<filename>', methods=['GET', 'POST'])
def get_ir(filename):
    return flask.send_from_directory(tonefinder.app.config['IR_FOLDER'],
                                     filename)

@tonefinder.app.route('/transformed_file/<filename>', methods=['GET', 'POST'])
def get_transformed(filename):
    return flask.send_from_directory(tonefinder.app.config['TRANSFORMED_FOLDER'],
                                     filename)

@tonefinder.app.route('/uploads/<filename>')
def get_image(filename):
    """Get image."""
    if not os.path.isfile(os.path.join(tonefinder.app.config['UPLOAD_FOLDER'],
                                       filename)):
        return flask.abort(404)
    return flask.send_from_directory(tonefinder.app.config['UPLOAD_FOLDER'],
                                     filename)