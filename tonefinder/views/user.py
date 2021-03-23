"""Insta485 file for users."""

import flask
import tonefinder


@insta485.app.route('/u/<user>/', methods=['GET', 'POST'])
def user_page(user):
    """User page."""
    logname = flask.session.get('username')
    if logname is None:
        return flask.redirect(flask.url_for('login'))
    if user is None:
        flask.abort(403)
    if flask.request.method == 'POST':
        conn = insta485.model.get_db()
        for key in flask.request.form:
            if key == 'follow':
                conn.execute(
                    "INSERT INTO following(username1, username2) \
                    VALUES (?,?);",
                    (logname, flask.request.form["username"])
                    )

            elif key == 'unfollow':
                conn.execute(
                    "DELETE FROM following \
                    WHERE username1 = ? AND username2 = ?;",
                    (logname, flask.request.form["username"])
                    )
        if 'file'in flask.request.files:
            filename = insta485.views.util.get_file()
            conn = insta485.model.get_db()
            posts = conn.execute("SELECT * FROM posts;")
            post_max = max(posts.fetchall(), key=lambda x: x['postid'])
            conn.execute(
                "INSERT INTO posts(postid, filename, owner) VALUES (?, ?, ?);",
                (post_max['postid'] + 1, filename, logname)
            )

    final_dict = dict()
    conn = insta485.model.get_db()
    pos = conn.execute(
        "SELECT postid, filename FROM posts WHERE owner=? \
        ORDER BY postid ASC;",
        (user,)
        )
    posts = pos.fetchall()
    num_post = len(posts)
    final_dict['logname'] = logname
    final_dict['username'] = user
    final_dict['total_posts'] = num_post
    final_dict['posts'] = posts
    log_follow = conn.execute(
        "SELECT username2 FROM following WHERE username1=?;",
        (logname,)
        )

    foll_list = log_follow.fetchall()
    final_dict['logname_follows_username'] = any(a['username2'] == user
                                                 for a in foll_list)
    followers = conn.execute(
        "SELECT username1 FROM following WHERE username2=?;",
        (user,))
    following = conn.execute(
        "SELECT username2 FROM following WHERE username1=?;",
        (user,)
        )
    final_dict['followers'] = len(followers.fetchall())
    final_dict['following'] = len(following.fetchall())
    user_fullname = conn.execute("SELECT fullname FROM users WHERE username=?",
                                 (user,))
    final_dict['fullname'] = user_fullname.fetchone()['fullname']
    return flask.render_template('user.html', **final_dict)

# -------------------------------------------------------------------------------


@insta485.app.route('/u/<user>/followers/', methods=['GET', 'POST'])
def followers_page(user):
    """followers."""
    logname = flask.session.get('username')

    if logname is None:
        return flask.redirect(flask.url_for('login'))
    if user is None:
        flask.abort(403)
    if flask.request.method == 'POST':
        # depending on unfollow or follow delete or update db
        conn = insta485.model.get_db()
        use = flask.request.form["username"]
        for key in flask.request.form:
            if key == 'follow':
                conn.execute(
                    "INSERT INTO following(username1, username2) \
                    VALUES (?,?);",
                    (logname, use)
                    )
            elif key == 'unfollow':
                conn.execute(
                    "DELETE FROM following \
                    WHERE username1 = ? AND username2 = ?;",
                    (logname, use)
                    )

    conn = insta485.model.get_db()
    fol = conn.execute(
        "SELECT F.username1 AS username, U.filename AS filename \
        FROM following F INNER JOIN users U ON U.username = F.username1 \
        WHERE F.username2 = ?;",
        (user,)
        )

    followers = fol.fetchall()
    for follower in followers:
        follower['handler'] = "get_image"
        follower['user_img_url'] = follower['filename']

        log_follow = conn.execute(
            "SELECT username2 FROM following \
            WHERE username1=? AND username2=?;",
            (logname, follower['username'])
            )

        foll_length = len(log_follow.fetchall())
        if foll_length == 0:
            follower['logname_follows_username'] = False
        else:
            follower['logname_follows_username'] = True

    final_dict = dict()
    final_dict['logname'] = logname
    final_dict['followers'] = followers
    return flask.render_template('followers.html', **final_dict)


# -------------------------------------------------------------------------------


@insta485.app.route('/u/<user>/following/', methods=['GET', 'POST'])
def following_page(user):
    """following."""
    logname = flask.session.get('username')

    if logname is None:
        return flask.redirect(flask.url_for('login'))
    if user is None:
        flask.abort(403)
    if flask.request.method == 'POST':
        # depending on unfollow or follow delete or update db
        use = flask.request.form["username"]
        conn = insta485.model.get_db()
        for key in flask.request.form:
            if key == 'follow':
                conn.execute(
                    "INSERT INTO following(username1, username2) \
                    VALUES (?,?);",
                    (logname, use)
                    )
            elif key == 'unfollow':
                conn.execute(
                    "DELETE FROM following \
                    WHERE username1 = ? AND username2 = ?;",
                    (logname, use)
                    )

    conn = insta485.model.get_db()
    fol = conn.execute(
        "SELECT F.username2 AS username, U.filename AS filename \
        FROM following F INNER JOIN users U ON U.username = F.username2 \
        WHERE F.username1 = ?;",
        (user,)
        )
    following = fol.fetchall()
    for follower in following:
        follower['handler'] = "get_image"
        follower['user_img_url'] = follower['filename']

        log_follow = conn.execute(
            "SELECT username2 FROM following \
            WHERE username1=? AND username2=?;",
            (logname, follower['username'])
            )
        foll_length = len(log_follow.fetchall())
        if foll_length == 0:
            follower['logname_follows_username'] = False
        else:
            follower['logname_follows_username'] = True

    final_dict = dict()
    final_dict['logname'] = logname
    final_dict['following'] = following
    return flask.render_template('following.html', **final_dict)
