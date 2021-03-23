"""
Insta485 index (main) view.

URLs include:
/
"""

import os
from operator import itemgetter
import arrow
import flask
import tonefinder


# -------------------------------------------------------------------------------


@insta485.app.route('/', methods=['GET', 'POST'])
def show_index():
    """Display / route."""
    if 'username' in flask.session:
        # Get the username
        user = flask.session['username']
        # Database portion
        conn = insta485.model.get_db()
        if flask.request.method == 'POST':
            for key in flask.request.form:
                if key == 'text':
                    comment_id = max(
                        conn.execute("SELECT * FROM comments").fetchall(),
                        key=lambda x: x['commentid'])['commentid'] + 1
                    conn.execute("INSERT INTO \
                                 comments(commentid, owner, postid, text) \
                                 VALUES (?, ?, ?, ?);",
                                 (comment_id, user,
                                  flask.request.form['postid'],
                                  flask.request.form[key]))

                elif key == 'like':
                    conn.execute("INSERT INTO likes(owner, postid) \
                                 VALUES (?,?);",
                                 (user, flask.request.form['postid']))
                elif key == 'unlike':
                    conn.execute("DELETE FROM likes WHERE postid = ? \
                                  AND owner = ?;",
                                 (flask.request.form['postid'], user))

        post_user = conn.execute("SELECT P.postid, P.filename, \
                                 P.owner, P.created \
                                 FROM posts P, following F \
                                 WHERE (F.username1 = ? AND \
                                 F.username2 = P.owner) \
                                 ORDER BY P.created DESC;",
                                 (user,))

        posts = conn.execute("SELECT * FROM posts P WHERE P.owner =?",
                             (user,)).fetchall()
        posts_user = post_user.fetchall()
        for i in posts_user:
            posts.append(i)
        posts = sorted(posts, key=itemgetter('postid'), reverse=True)

        for post in posts:
            likes = conn.execute("SELECT owner FROM likes WHERE postid = ?;",
                                 (post['postid'],))
            comment = conn.execute("SELECT C.commentid, C.owner, C.text \
                                    FROM comments C WHERE C.postid = ? \
                                    ORDER BY C.commentid",
                                   (post['postid'], ))

            profile_pic = conn.execute("SELECT filename FROM users \
                                        WHERE username = ?;",
                                       (post['owner'],))

            post['handler'] = "get_image"
            post['owner_img_url'] = profile_pic.fetchone()['filename']
            post['comments'] = comment.fetchall()
            like_list = likes.fetchall()
            post['likes'] = len(like_list)
            post['like'] = not any(a['owner'] == user for a in like_list)
            created_time = arrow.get(post['created'], 'YYYY-MM-DD HH:mm:ss')
            post['timestamp'] = created_time.humanize(arrow.utcnow())
        final_dict = dict()
        final_dict['posts'] = posts
        final_dict['logname'] = user
        return flask.render_template("index.html", **final_dict)
    return flask.redirect(flask.url_for('login'))


# -------------------------------------------------------------------------------


@insta485.app.route('/p/<postid>/', methods=['GET', 'POST'])
def post_page(postid):
    """Posts."""
    if 'username' in flask.session:
        # Get the username
        user = flask.session['username']
        if flask.request.method == 'POST':
            conn = insta485.model.get_db()
            for key in flask.request.form:
                if key == 'text':
                    comment_id = len(
                        conn.execute("SELECT * FROM comments").fetchall()) + 1
                    conn.execute("INSERT INTO \
                                  comments(commentid, owner, postid, text) \
                                  VALUES (?, ?, ?, ?);",
                                 (comment_id, user,
                                  flask.request.form['postid'],
                                  flask.request.form[key]))
                elif key == 'like':
                    conn.execute("INSERT INTO likes(owner, postid) \
                                  VALUES (?,?);",
                                 (user, flask.request.form['postid']))
                elif key == 'unlike':
                    conn.execute("DELETE FROM likes WHERE postid = ? \
                                 AND owner = ?;",
                                 (flask.request.form['postid'], user))
                elif key == 'commentid':
                    conn.execute("DELETE FROM comments WHERE commentid = ?",
                                 (flask.request.form[key],))
                elif key == 'delete':
                    post_filename = conn.execute(
                        "SELECT filename FROM posts \
                        WHERE postid=?;",
                        (postid, )).fetchone()['filename']
                    # post_filename = post.fetchone()['filename']
                    post_path = os.path.join(
                        insta485.app.config["UPLOAD_FOLDER"],
                        post_filename
                    )
                    os.unlink(post_path)
                    conn.execute("DELETE FROM posts WHERE postid=?;",
                                 (postid, ))

        final_dict = dict()
        conn = insta485.model.get_db()
        post = conn.execute('SELECT * FROM posts WHERE postid=?;',
                            (postid,))
        post = post.fetchone()
        if post is None:
            return flask.redirect(flask.url_for('login'))
        post_dict = post
        profile_pic = conn.execute('SELECT filename FROM users \
                                   WHERE username=?',
                                   (post['owner'],))
        post_dict['owner_img_url'] = profile_pic.fetchone()['filename']

        likes = conn.execute("SELECT owner FROM likes WHERE postid = ?;",
                             (post['postid'],))

        comment = conn.execute("SELECT C.commentid, C.owner, C.text \
                                FROM comments C WHERE C.postid = ? \
                                ORDER BY C.commentid",
                               (post['postid'], ))

        post_dict['comments'] = comment.fetchall()
        like_list = likes.fetchall()
        post_dict['likes'] = len(like_list)
        post_dict['like'] = not any(a['owner'] == user for a in like_list)
        created_time = arrow.get(post['created'], 'YYYY-MM-DD HH:mm:ss')
        post_dict['timestamp'] = created_time.humanize(arrow.utcnow())
        final_dict['post'] = post_dict
        final_dict['logname'] = user
        return flask.render_template("post.html", **final_dict)
    return flask.redirect(flask.url_for('login'))


# -------------------------------------------------------------------------------


@insta485.app.route('/explore/', methods=['GET', 'POST'])
def explore_page():
    """Explore."""
    if 'username' in flask.session:
        # Get the username
        logname = flask.session['username']

        if flask.request.method == 'POST':
            # gotta update followers list
            follow_user = flask.request.form["username"]
            conn = insta485.model.get_db()
            conn.execute("INSERT INTO following(username1, username2)\
                        VALUES (?, ?);", (logname, follow_user))
        conn = insta485.model.get_db()
        fol = conn.execute("SELECT username2 FROM following WHERE \
                            username1 = ?",
                           (logname,))

        following = fol.fetchall()
        use = conn.execute("SELECT username, filename FROM users")
        users = use.fetchall()
        temp_dict = []
        for user in users:
            if not any(d['username2'] == user['username'] for d in following) \
               and user['username'] != logname:
                temp_dict.append({'user_img_url': user['filename'],
                                  'username': user['username']})
        final_dict = dict()
        final_dict['logname'] = logname
        final_dict['not_following'] = temp_dict
        return flask.render_template("explore.html", **final_dict)
    if flask.request.method == 'POST':
        flask.abort(403)
    return flask.redirect(flask.url_for('login'))


# -------------------------------------------------------------------------------


@insta485.app.route('/uploads/<filename>')
def get_image(filename):
    """Get image."""
    if not os.path.isfile(os.path.join(insta485.app.config['UPLOAD_FOLDER'],
                                       filename)):
        return flask.abort(404)
    return flask.send_from_directory(insta485.app.config['UPLOAD_FOLDER'],
                                     filename)
