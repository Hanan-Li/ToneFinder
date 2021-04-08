"""REST API for v1."""
import flask
import tonefinder


@tonefinder.app.route('/api/v1/p/<int:postid_url_slug>/comments/',
                    methods=["GET", "POST"])
def get_comments(postid_url_slug):
    """Return likes on postid.

    Example:
    {
        "posts": "/api/v1/p/",
        "url": "/api/v1/"
    }
    """
    context = {}
    if tonefinder.model.check_403(context, flask.session):
        return flask.jsonify(**context), 403
    connection = tonefinder.model.get_db()
    cur = connection.execute(
        "SELECT EXISTS(SELECT * FROM posts WHERE postid = ?) AS pogchamp;",
        (postid_url_slug,)
    )
    exists = cur.fetchone()["pogchamp"]
    if tonefinder.model.check_404(context, exists):
        return flask.jsonify(**context), 404
    # User
    logname = flask.session['username']
    if flask.request.method == "POST":
        data = flask.request.get_json()
        text = data["text"]
        cur = connection.execute(
            "SELECT commentid FROM comments ORDER BY commentid DESC LIMIT 1;"
        )
        last_id = cur.fetchone()["commentid"] + 1
        cur = connection.execute(
            "INSERT INTO comments(commentid, owner, postid, text) "
            "VALUES (?,?,?,?);",
            (last_id, logname, postid_url_slug, text)
        )
        context["commentid"] = last_id
        context["owner"] = logname
        context["owner_show_url"] = "/u/" + logname + "/"
        context["postid"] = postid_url_slug
        context["text"] = text
        return flask.jsonify(**context), 201

    cur = connection.execute(
        "SELECT * FROM comments WHERE postid = ? ORDER BY commentid ASC;",
        (postid_url_slug,)
    )
    comments = cur.fetchall()
    com_list = []
    for comment in comments:
        com_dict = {}
        com_dict["commentid"] = comment["commentid"]
        com_dict["owner"] = comment["owner"]
        com_dict["owner_show_url"] = "/u/" + comment["owner"] + "/"
        com_dict["postid"] = postid_url_slug
        com_dict["text"] = comment["text"]
        com_list.append(com_dict)
    context["comments"] = com_list
    context["url"] = flask.request.path
    return flask.jsonify(**context)
