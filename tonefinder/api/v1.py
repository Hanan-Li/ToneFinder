"""REST API for v1."""
import flask
import tonefinder


@insta485.app.route('/api/v1/', methods=["GET"])
def get_v1():
    """Return likes on postid.

    Example:
    {
        "posts": "/api/v1/p/",
        "url": "/api/v1/"
    }
    """
    context = {}
    if insta485.model.check_403(context, flask.session):
        return flask.jsonify(**context), 403
    # User

    # url
    context["posts"] = "/api/v1/p/"
    context["url"] = flask.request.path

    return flask.jsonify(**context)
