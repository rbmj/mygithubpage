import sqlite3

from flask import Flask, render_template, request, redirect, make_response, g, session

app = Flask(__name__)

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = sqlite3.connect('users.db')
  return db

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()

def do_login(user, password, admin):
  resp = make_response(redirect('/'))
  session['user'] = user
  session['admin'] = admin
  return resp

@app.route('/')
def index():
  return render_template('index.html', user = session.get('user', None))

@app.route('/login', methods=['POST'])
def login():
  user =  request.form.get('user', '')
  password = request.form.get('password', '')

  c = get_db().cursor()
  statement = "SELECT * FROM users WHERE name ='" + user + "'"
  result = c.execute(statement).fetchone()
  if result == None:
    return render_template('error.html', error = 'Invalid user'), 403
  if result[1] != password:
    return render_template('error.html', error = 'Invalid password'), 403
  else:
    return do_login(user, password, result[2])

@app.route('/logout', methods=['GET'])
def logout():
  resp = make_response(redirect('/'))
  session.pop('user', None)
  session.pop('admin', None)
  return resp

import os
app.secret_key = os.urandom(24)

if __name__ == '__main__':
  app.run(debug = True)
