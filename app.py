from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort


app = Flask(__name__)

 ### Define a conexão com o banco de dados

def get_db_connection():
    conw = None
    connw = sqlite3.connect('EstufaDB.db')
    connw.row_factory = sqlite3.Row

    return connw

 ### Apontamento de rotas
@app.route('/')
def index():

    connw = get_db_connection()
    posts_humid = connw.execute('SELECT * FROM humid ORDER BY ID DESC LIMIT 1').fetchall()
    posts_dht11 = connw.execute('SELECT * FROM dht11 ORDER BY ID DESC LIMIT 1').fetchall()
    posts_reserv = connw.execute('SELECT * FROM reserv ORDER BY ID DESC LIMIT 1').fetchall()
    posts_log = connw.execute('SELECT * FROM log_estufa ORDER BY ID DESC LIMIT 5').fetchall()
    connw.close()

    try:
        if request.args['teste'] == '1':
            print("deu boaaaaa 111111111111")
        elif request.args['teste'] == '2':
            print("deu boaaaaa 222222222222")
        elif request.args['teste'] == '3':
            print("deu boaaaaa 333333333333")
    except:
        pass

    return render_template('index.html', posts_humid=posts_humid, posts_dht11=posts_dht11, posts_reserv=posts_reserv, posts_log=posts_log)

@app.route('/humid')
def post_humid():
    post_humid = get_post_humid()
    return render_template('humid.html', post_humid=post_humid)

@app.route('/dht11')
def post_dht11():
    post_dht11 = get_post_dht11()
    return render_template('dht11.html', post_dht11=post_dht11)

@app.route('/reserv')
def post_reserv():
    post_reserv = get_post_reserv()
    return render_template('reserv.html', post_reserv=post_reserv)

 ### Definições das funções WEB

def get_post_humid():
    connw = get_db_connection()
    post_humid = connw.execute('SELECT * FROM humid ORDER BY ID DESC LIMIT 17').fetchall()
    connw.close()
    print(post_humid)
    if post_humid is None:
        abort(404)
    return post_humid

def get_post_dht11():
    connw = get_db_connection()
    post_dht11 = connw.execute('SELECT * FROM dht11 ORDER BY ID DESC LIMIT 17').fetchall()
    connw.close()
    if post_dht11 is None:
        abort(404)
    return post_dht11
    
def get_post_reserv():
    connw = get_db_connection()
    post_reserv = connw.execute('SELECT * FROM reserv ORDER BY ID DESC LIMIT 17').fetchall()
    connw.close()
    if post_reserv is None:
        abort(404)
    return post_reserv



    #validar a inclusão de uma pagina para marcar o inicio do cultivo, para poder apresentar 