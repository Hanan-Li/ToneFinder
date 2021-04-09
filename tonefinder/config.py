"""
Insta485 development configuration.

Andrew DeOrio <awdeorio@umich.edu>
"""

import os

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
K = b'\x95\x92\x80y\xd3\x12\xd7\xca\xe6\x99JuI\xf7k\x89\xf7\xbd\x9f\xc3[1Zp'
SECRET_KEY = K
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
IR_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'ir'
)

GUITAR_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'guitar'
)

TRANSFORMED_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'transformed'
)


ALLOWED_EXTENSIONS = set(['wav'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/insta485.sqlite3
DATABASE_FILENAME = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'insta485.sqlite3'
)
