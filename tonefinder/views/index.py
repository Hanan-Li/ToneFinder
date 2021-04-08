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
            if src_file is not None and ref_file is not None:
                mg.process(
                    target=src_file,
                    reference=ref_file,
                    # pcm16 and pcm24 are just basic shortcuts
                    # You can also use the Result class to make some advanced results
                    results=[
                        mg.Result(
                            "custom_result_24bit_no_limiter.wav", subtype="PCM_24", use_limiter=False
                        ),
                    ],
                    ir_file = "mid_ir.wav"
                )
        return flask.render_template("index.html", **final_dict)
    else:
        return flask.redirect(flask.url_for('login'))
    # return flask.redirect(flask.url_for('login'))



# -------------------------------------------------------------------------------


# @insta485.app.route('/uploads/<filename>')
# def get_image(filename):
#     """Get image."""
#     if not os.path.isfile(os.path.join(insta485.app.config['UPLOAD_FOLDER'],
#                                        filename)):
#         return flask.abort(404)
#     return flask.send_from_directory(insta485.app.config['UPLOAD_FOLDER'],
#                                      filename)
