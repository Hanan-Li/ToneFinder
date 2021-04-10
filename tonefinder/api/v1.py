"""REST API for v1."""
import flask
import tonefinder


@tonefinder.app.route('/api/v1/save_ir', methods=["POST"])
def save_ir():
    """Return likes on postid.

    Example:
    {
        "posts": "/api/v1/p/",
        "url": "/api/v1/"
    }
    """
    context = {}
    if tonefinder.model.check_403(context, flask.session):
        context["error"] = "unauthorized access"
        return flask.jsonify(**context), 403
    # User
    username = flask.session['username']
    if flask.request.method == "POST":
        data = flask.request.get_json()
        print(data)
        name = data["name"]
        ir_file = data["ir_file"]
        conn = tonefinder.model.get_db()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO `ir` (`name`, `irfile`, `owner`) VALUES (%s, %s, %s)""",(name, ir_file, username))
        conn.commit()
        context["created"] = True
        context["name"] = name
        context["file"] = ir_file
    # url
    return flask.jsonify(**context)


@tonefinder.app.route('/api/v1/get_guitar_profile', methods=["GET"])
def get_guitar_profile():
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
    username = flask.session['username']
    if flask.request.method == "GET":
        conn = tonefinder.model.get_db()
        cursor = conn.cursor()
        cursor.execute("""SELECT name, guitarfile FROM guitar WHERE owner=%s""", (username,))
        guitar_info = cursor.fetchall()
        context["username"] = username
        context["guitar_files"] = []
        for guitar_profile in guitar_info:
            context["guitar_files"].append(guitar_profile)
    return flask.jsonify(**context)


@tonefinder.app.route('/api/v1/get_ir', methods=["GET"])
def get_ir_profile():
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
    username = flask.session['username']
    if flask.request.method == "GET":
        conn = tonefinder.model.get_db()
        cursor = conn.cursor()
        cursor.execute("""SELECT name, irfile FROM ir WHERE owner=%s""", (username,))
        ir_info = cursor.fetchall()
        print(ir_info)
        context["username"] = username
        context["ir_files"] = []
        for ir_profile in ir_info:
            context["ir_files"].append(ir_profile)
    return flask.jsonify(**context)