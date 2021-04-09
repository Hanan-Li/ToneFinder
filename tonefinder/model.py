"""Insta485 model (database) API."""
import sqlite3
import MySQLdb
import MySQLdb.cursors
import flask
import tonefinder


def get_db():
    """Open a new database connection."""
    if not hasattr(flask.g, 'db'):
        flask.g.sqlite_db = MySQLdb.connect(host="tf-db.czjdy4yl1hn3.us-east-2.rds.amazonaws.com",user="admin", passwd="Bee_dave_1998",db="tonefinder", cursorclass=MySQLdb.cursors.DictCursor)
    return flask.g.sqlite_db


@tonefinder.app.teardown_appcontext
def close_db(error):
    # pylint: disable=unused-argument
    """Close the database at the end of a request."""
    if hasattr(flask.g, 'db'):
        flask.g.sqlite_db.commit()
        flask.g.sqlite_db.close()


def check_403(context, session):
    """Check for 403."""
    if 'username' not in session:
        context["message"] = "Forbidden"
        context["status_code"] = 403
        return True
    return False


def check_404(context, exists):
    """Check for 404."""
    if not exists:
        context["message"] = "Not Found"
        context["status_code"] = 404
        return True
    return False
