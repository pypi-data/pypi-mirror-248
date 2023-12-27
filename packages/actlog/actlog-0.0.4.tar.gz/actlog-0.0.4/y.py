import sys

from enum import Enum

class Color(Enum):
    RED=1
    BLUE=2

def foo(a : Color) -> str:
    return a


def lort(a:int) -> int:
    return a

lort("str")

print(foo(Color.BLUE))
print(foo('sub'))


r = Color.RED

print(hasattr(Color, 'RED'))
print(hasattr(Color, 'YELLOW'))
# print('YELLOW' in Color)
r1 = Color['RED']
r2 = Color.RED
print(r1 == r2)
y = Color['YELLOW']


sys.exit(0)

import bcrypt
import getpass
import os
from hashlib import scrypt
import secrets


from flask import Flask, session, request

app = Flask(__name__)

# app.secret_key = 'BAD_SECRET_KEY'

app.config['SECRET_KEY'] = 'BAD_SECRET_KEY2'
app.config['SESSION_COOKIE_NAME'] = 'actlog-session'
app.config['SESSION_COOKIE_HTTPONLY'] = False


def get_foobar():
    # print(type(request.url))
    if not "foobar" in session:
        session['foobar'] = os.urandom(16).hex()
    return session['foobar']

@app.route("/")
def hello_world():
    # session['email'] = request.form['email_address']
    session['loggedin'] = False
    js = """
    <script>
        function getCookie(name) {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        }
        let actlogCookieString = getCookie('actlog-session')
        base64 = actlogCookieString.split('.')[0]
        actlogCookie = JSON.parse(atob(base64))
        console.log(actlogCookie)
    </script>
    """
    return f"{js}<p>Hello, World! {get_foobar()}</p>"

# salt = os.urandom(16)
# 
# encoded = scrypt('foobar'.encode(), salt=salt, n=2048, r=8, p=1)
# print(encoded.hex())
# password = getpass.getpass("password: ")
# hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
# print(hashed_password.decode())