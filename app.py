from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('EstufaDB.db')
    conn.row_factory = sqlite3.Row

    return conn

@app.route('/')
def index():

    conn = get_db_connection()
    posts_humid = conn.execute('SELECT * FROM humid ORDER BY ID DESC LIMIT 1').fetchall()
    posts_dht11 = conn.execute('SELECT * FROM dht11 ORDER BY ID DESC LIMIT 1').fetchall()
    posts_reserv = conn.execute('SELECT * FROM reserv ORDER BY ID DESC LIMIT 1').fetchall()
    conn.close()

    return render_template('index.html', posts_humid=posts_humid, posts_dht11=posts_dht11, posts_reserv=posts_reserv)

@app.route('/humid')
def post_humid():
    post_humid = get_post_humid()
    return render_template('humid.html', post_humid=post_humid)

@app.route('/dht11')
def post_dht11():
    post_dht11 = get_post_dht11()
    return render_template('dht11.html', post_dht11=post_dht11)

# def teste(str_teste):
#     str_teste = str_teste
#     print(str_teste)


def get_post_humid():
    conn = get_db_connection()
    post_humid = conn.execute('SELECT * FROM humid ORDER BY ID DESC LIMIT 17').fetchall()
    conn.close()
    print(post_humid)
    if post_humid is None:
        abort(404)
    return post_humid

def get_post_dht11():
    conn = get_db_connection()
    post_dht11 = conn.execute('SELECT * FROM dht11 ORDER BY ID DESC LIMIT 17').fetchall()
    conn.close()
    if post_dht11 is None:
        abort(404)
    return post_dht11