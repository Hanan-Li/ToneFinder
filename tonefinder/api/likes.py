"""REST API for likes."""
import flask
import insta485


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/likes/',
                    methods=["GET", "POST", "DELETE"])
def get_likes(postid_url_slug):
    """Return likes on postid.

    Example:
    {
      "logname_likes_this": 1,
      "likes_count": 3,
      "postid": 1,
      "url": "/api/v1/p/1/likes/"
    }
    """
    context = {}
    if insta485.model.check_403(context, flask.session):
        return flask.jsonify(**context), 403
    # User
    logname = flask.session['username']
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT EXISTS(SELECT * FROM posts WHERE postid = ?) AS pog;",
        (postid_url_slug,)
    )
    exists = cur.fetchone()["pog"]
    if not exists:
        context["message"] = "Not Found"
        context["status_code"] = 404
        return flask.jsonify(**context), 404
    if flask.request.method == "POST":
        cur = connection.execute(
            "SELECT EXISTS( "
            "  SELECT 1 FROM likes "
            "    WHERE postid = ? "
            "    AND owner = ? "
            "    LIMIT 1"
            ") AS logname_likes_this ",
            (postid_url_slug, logname)
        )
        is_like = cur.fetchone()["logname_likes_this"]
        if is_like:
            context["logname"] = logname
            context["message"] = "Conflict"
            context["postid"] = postid_url_slug
            context["status_code"] = 409
            return flask.jsonify(**context), 409

        cur = connection.execute(
            "INSERT INTO likes(owner, postid)"
            "VALUES (?, ?);",
            (logname, postid_url_slug)
        )
        context["logname"] = logname
        context["postid"] = postid_url_slug
        return flask.jsonify(**context), 201

    if flask.request.method == "DELETE":
        cur = connection.execute(
            "SELECT EXISTS( "
            "  SELECT 1 FROM likes "
            "    WHERE postid = ? "
            "    AND owner = ? "
            "    LIMIT 1"
            ") AS logname_likes_this ",
            (postid_url_slug, logname)
        )
        is_like = cur.fetchone()["logname_likes_this"]
        if is_like:
            cur = connection.execute(
                "DELETE FROM likes WHERE owner=? AND postid=?",
                (logname, postid_url_slug)
            )
        return '', 204

    # url
    context["url"] = flask.request.path

    # Post
    postid = postid_url_slug
    context["postid"] = postid

    # Did this user like this post?
    cur = connection.execute(
        "SELECT EXISTS( "
        "  SELECT 1 FROM likes "
        "    WHERE postid = ? "
        "    AND owner = ? "
        "    LIMIT 1"
        ") AS logname_likes_this ",
        (postid, logname)
    )
    logname_likes_this = cur.fetchone()
    context.update(logname_likes_this)

    # Likes
    cur = connection.execute(
        "SELECT COUNT(*) AS likes_count FROM likes WHERE postid = ? ",
        (postid,)
    )
    likes_count = cur.fetchone()
    context.update(likes_count)
    return flask.jsonify(**context)
