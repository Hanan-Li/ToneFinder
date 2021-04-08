"""Insta485 utility files."""

import os
import shutil
import tempfile
import hashlib
import uuid
import flask
import tonefinder


# UTILITY
# -------------------------------------------------------------------------------
def sha256sum(filename):
    """Return sha256 hash of file content, similar to UNIX sha256sum."""
    content = open(filename, 'rb').read()
    sha256_obj = hashlib.sha256(content)
    return sha256_obj.hexdigest()


def sha512(password):
    """sha512."""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    print(password_db_string)
    return password_db_string


def pseudosha(algorithm, salt, password):
    """pseudosha."""
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    print(password_db_string)
    return password_db_string


def get_file():
    """Get File."""
    filename = ''
    if flask.request.files.get('file') is not None:
        dummy, temp_filename = tempfile.mkstemp()
        file = flask.request.files["file"]
        file.save(temp_filename)
        # Compute filename
        hash_txt = tonefinder.views.util.sha256sum(temp_filename)
        dummy, suffix = os.path.splitext(file.filename)
        hash_filename_basename = hash_txt + suffix
        hash_filename = os.path.join(
            tonefinder.app.config["UPLOAD_FOLDER"],
            hash_filename_basename
        )

        # Move temp file to permanent location
        shutil.move(temp_filename, hash_filename)
        filename = hash_filename_basename
    return filename

def save_file():
    src_filname = ''
    ref_filename = ''
    if flask.request.files.get('source') is not None:
        dummy, temp_filename = tempfile.mkstemp()
        file = flask.request.files["source"]
        file.save(temp_filename)
        src_filname = temp_filename
    if flask.request.files.get('reference') is not None:
        dummy, temp_filename = tempfile.mkstemp()
        file = flask.request.files["reference"]
        file.save(temp_filename)
        ref_filename = temp_filename
    return src_filname, ref_filename
    
