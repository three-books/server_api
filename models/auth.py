import sqlite3

from flask import Flask
from flask import g

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('./db/server_api.db')
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def login(id, password):
    db = get_db()
    curs = db.cursor()
    curs.execute(f'SELECT ID FROM ACCOUNT WHERE ID="{id}" AND PASSWORD="{password}";')
    # sql = 'SELECT ID FROM ACCOUNT WHERE ID=? AND PASSWORD=?;'
    # curs.execute(sql, (id, password))
    result = 'True' if curs.fetchone() else ''
    curs.close()

    return result


