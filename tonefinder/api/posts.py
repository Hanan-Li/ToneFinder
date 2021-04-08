"""REST API for v1."""
import flask
import tonefinder


@tonefinder.app.route('/api/v1/p/', methods=["GET"])
def get_posts():
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
    # User
    size = 10
    page = 0
    size_set = False
    if "size" in flask.request.args:
        size_set = True
        size = int(flask.request.args["size"])
    if "page" in flask.request.args:
        page = int(flask.request.args["page"])
    # CHECK IF SIZE AND PAGE ARE NON NEGATIVE
    logname = flask.session['username']
    if size < 0 or page < 0:
        context["message"] = "Bad Request"
        context["status_code"] = 400
        return flask.jsonify(**context), 400
    # url
    context["next"] = ""
    connection = tonefinder.model.get_db()
    # cur = connection.execute("SELECT postid FROM posts WHERE postid = 1;")

    cur = connection.execute(
        "SELECT * FROM posts WHERE "
        "(EXISTS(SELECT * FROM following F "
        "WHERE F.username1 = ? AND F.username2 = owner) "
        "OR owner = ?) ORDER BY postid DESC "
        "LIMIT ? OFFSET ?;",
        (logname, logname, size, page*size)
        )
    posts = cur.fetchall()
    post_list = []
    cur = connection.execute(
        "SELECT * FROM posts WHERE "
        "(EXISTS(SELECT * FROM following F "
        "WHERE F.username1 = ? AND F.username2 = owner) "
        "OR owner = ?) ORDER BY postid DESC "
        "LIMIT ? OFFSET ?;",
        (logname, logname, size, (page+1)*size)
        )
    next_post = cur.fetchall()
    post_len = len(next_post)
    if post_len != 0:
        temp = "/api/v1/p/?page=" + str(page+1)
        if size_set:
            temp = "/api/v1/p/?size=" + str(size) + "&page=" + str(page+1)
        context["next"] = temp
    else:
        context["next"] = ""
    for post in posts:
        post_dic = {}
        post_dic["postid"] = post["postid"]
        post_dic["url"] = "/api/v1/p/" + str(post["postid"]) + "/"
        post_list.append(post_dic)

    context["results"] = post_list
    context["url"] = flask.request.path

    return flask.jsonify(**context)
