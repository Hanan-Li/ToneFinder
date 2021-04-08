"""REST API for v1."""
import flask
import tonefinder


@tonefinder.app.route('/api/v1/p/<int:postid_url_slug>/', methods=["GET"])
def get_postid(postid_url_slug):
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
    connection = tonefinder.model.get_db()
    cur = connection.execute(
        "SELECT EXISTS(SELECT * FROM posts WHERE postid = ?) AS kek;",
        (postid_url_slug,)
    )
    exists = cur.fetchone()["kek"]
    if tonefinder.model.check_404(context, exists):
        return flask.jsonify(**context), 404

    cur = connection.execute(
        "SELECT P.created AS age, P.filename AS img_url, P.owner, \
        U.filename AS owner_img_url, P.postid FROM posts P \
        INNER JOIN users U ON U.username = P.owner WHERE P.postid = ?;",
        (postid_url_slug,)
    )
    post = cur.fetchone()
    context["age"] = post["age"]
    context["img_url"] = "/uploads/" + post["img_url"]
    context["owner"] = post["owner"]
    context["owner_img_url"] = "/uploads/" + post["owner_img_url"]
    context["owner_show_url"] = "/u/" + post["owner"] + "/"
    context["post_show_url"] = "/p/" + str(post["postid"]) + "/"
    context["url"] = flask.request.path

    return flask.jsonify(**context)
