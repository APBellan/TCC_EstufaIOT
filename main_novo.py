from string import Template
from typing import Type
import RPi.GPIO as gpio
import paho.mqtt.client as mqtt
import serial
import threading
import time as time
import datetime as dt
from datetime import datetime
import Adafruit_DHT as dht
import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from variaveis import *    #iniciar variaveis iniciais -- Outras variaveis que não aparecem aqui 
                           #                              estão definidas no arquivo variaveis.py


#*********************************************************************************
            #******************    WEB APP    ******************
#*********************************************************************************

app = Flask(__name__)

 ### Define a conexão com o banco de dados

def get_db_connection():
    conw = None
    connw = sqlite3.connect(db_file)
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
    connw = get_db_connection(r"EstufaDB.db")
    post_humid = connw.execute('SELECT * FROM humid ORDER BY ID DESC LIMIT 17').fetchall()
    connw.close()
    print(post_humid)
    if post_humid is None:
        abort(404)
    return post_humid

def get_post_dht11():
    connw = get_db_connection(r"EstufaDB.db")
    post_dht11 = connw.execute('SELECT * FROM dht11 ORDER BY ID DESC LIMIT 17').fetchall()
    connw.close()
    if post_dht11 is None:
        abort(404)
    return post_dht11
    
def get_post_reserv():
    connw = get_db_connection(r"EstufaDB.db")
    post_reserv = connw.execute('SELECT * FROM reserv ORDER BY ID DESC LIMIT 17').fetchall()
    connw.close()
    if post_reserv is None:
        abort(404)
    return post_reserv



#*********************************************************************************
        #******************    Gerencimento da Estufa    ******************
#*********************************************************************************



    #Verificar variaveis
arduino = serial.Serial('/dev/ttyACM0', 9600) #inicia a comunicação serial com o arduino
dht_sensor = dht.DHT11
# bkrMqtt = mqtt.Client("ESTUFABROKER") # define o nome do cliente MQTT



                # definição dos pinos
gpio.setmode(gpio.BCM)


    #rele1 / utilizado para ligar o cooler
# rele1 = 12
# gpio.setup(rele1, gpio.OUT)
# gpio.output(rele1, 1)

    #rele2 / utilizado para ligar a irrigação
# rele2 = definir pino   
# gpio.setup(rele2, gpio.OUT)
# gpio.output(rele2, 1)

    #rele3 / utilizado para ligar a luz
# rele3 = definir pino 
# gpio.setup(rele3, gpio.OUT)
# gpio.output(rele3, 1)

   # variaveis de tempo

t10s = dt.timedelta(seconds=10)
t30s = dt.timedelta(seconds=30)
t01m = dt.timedelta(minutes=1)
t05m = dt.timedelta(minutes=5)
t10m = dt.timedelta(minutes=10)
t30m = dt.timedelta(minutes=30)

#horaltr_humid = datetime.datetime.now()   # define start tempo leitores de umidade
#horaltr_dht11 = dt.datetime.now()    # define start tempo dht11
horaltr_reserv = dt.datetime.now()   # define start tempo ultrasomico reservatorio de agua


    #configuração DHT11
pin_dht11 = 24 # DHT11  /  Biblioteca usa modo BCM


#*********************************************************************************
      #******************    Definições das funções    ******************
#*********************************************************************************

#                 # Conexão com o Broker MQTT Mosquitto
# def mqtt_client_connect():
#     try:
#         #print("connected to: ", broker_url)
#         bkrMqtt.connect(broker_url)
#         bkrMqtt.loop_start()
#         return True
#     except:
#         print("erro ao se conectar com o Broker MQTT")
#         pass
#     return


 ### inicia conexão com o banco de dados
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        #print(sqlite3.version)
    except Error as e:
        print(e)

    return conn
    # finally:
    #     if conn:
    #         conn.close()


            # Insere dados dentro do DB
def db_humid(conn, humid):
    """
    Create a new humid into the humids table
    :param conn:
    :param humid:
    :return: humid id
    """
    sql = ''' INSERT INTO humid(humid,datahumid)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, humid)
    conn.commit()
    return cur.lastrowid

        # Insere dados dentro do DB
def db_dht11(conn, dht11):
    """
    Create a new dht11
    :param conn:
    :param dht11:
    :return:
    """

    sql = ''' INSERT INTO dht11(temp,humid,datadht11)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, dht11)
    conn.commit()
    return cur.lastrowid

def db_reserv(conn, reserv):
    """
    Create a new reserv
    :param conn:
    :param reserv:
    :return:
    """

    sql = ''' INSERT INTO reserv(reserv,datareserv)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, reserv)
    conn.commit()
    return cur.lastrowid

def db_irrig(conn, irrig):
    """
    Create a new irrig
    :param conn:
    :param irrig:
    :return:
    """

    sql = ''' INSERT INTO irrig(irrig,datairrig)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, irrig)
    conn.commit()
    return cur.lastrowid


def get_data(conn, tabela):
    # ***************    função responsavel por pegar a ultima data do banco    *********************
    try:
            
        #conn = create_connection(r"EstufaDB.db") # inicia conexão com o banco

        cursor = conn.cursor()
        
        # lendo os dados
        cursor.execute(f"""
        SELECT data{tabela} FROM {tabela} ORDER BY ID DESC LIMIT 1;
        """)
        for linha in cursor.fetchall():
            data = linha[0]
        #print(data)
        #conn.close()  # Finaliza a conexão com o banco
    except:
        print("erro DB data_humid")
    
    return data

                # Pegar dados do arduino e devolver uma variavel
def dados_arduino(item):
    try:
        arduino.write(item.encode())
        msg = int(arduino.readline()) #Lê os dados em formato de inteiro
        print(f"valor lido do sensor {item}: {msg}%") #Imprime a mensagem
        return msg
    except:
        print(f"impossivel receber humidade do sensor{item}")
        return 0    

               
def dados_reserv():
                   # Pegar dados do arduino e devolver uma variavel
    try:
        arduino.write('a'.encode())
        msgr = float(arduino.readline()) #Lê os dados em formato de float
        print(f"valor lido do sensor: {msgr}%") #Imprime a mensagem
        return msgr
    except:
        print(f"impossivel receber volume do reservatorio{item}")
        return 0    

def dados_humid():
                      #Tratar dados da humidade da terra  
    resultado_humidade.clear()
    try:
        for item in cont_sensors_humid:
            lidoard = dados_arduino(item) # armazena o valor
            arduino.flush() #Limpa a comunicação
            #print(lidoard)
            if lidoard != 0 and lidoard is not None: # gravar apenas os dados diferentes de 0
                resultado_humidade.append(lidoard) #grava os dados em uma lista
                #print(resultado_humidade)
            else:
                print("valores dos sensores invalidos")
        qtd_dados_humid = len(resultado_humidade) #verifica quantos dados validos foram recebidos
        #print(qtd_dados_humid)
        #int_list = (map(int, resultado_humidade)) #converte a string em int
        #print(resultado_humidade)
        humid_media = int(sum(resultado_humidade) / qtd_dados_humid) #gera a humidade média dos sensores
        #print(f'Humidade Média: {humid_media}%')
  
    except ZeroDivisionError:
        print('divisao impossivel')
    return humid_media  
                  
def dados_dht11(humid_dht11, temp):
             # realiza a leitura do DHT11    
             
    humid_dht11, temp = dht.read_retry(dht_sensor, pin_dht11)
    if humid_dht11 is not None and temp is not None:
        humid_dht11 = int(humid_dht11)
        temp = int(temp)
        print(f"Temperatura={temp}*C  Umidade={humid_dht11}%")
        # bkrMqtt.publish(temperature_topic, temp)
        # bkrMqtt.publish(humidity_topic, humid)
    else:
        print("Falha ao receber os dados do sensor de umidade")

    return humid_dht11, temp

#*********************************************************************************
            #******************    LOOP PRINCIPAL    ******************
#*********************************************************************************

try:    
    print("Aprerte Ctrl + C para termiar")
    time.sleep(3)
    while True:

                    # Inicia a comunicação com o Brocker
        
        conectividade = mqtt_client_connect()   #inicia conexão mqtt

        if conectividade == True:    #valida se esta conectado ao broker
            
  # ***************    get humidade media    *********************

            conn = create_connection(r"EstufaDB.db")

            horaltr_humid = get_data(conn, tb_humid)
            horaltr_humid = datetime.strptime(horaltr_humid, '%Y-%m-%d %H:%M:%S.%f')

            #print(f"data DB humid = {horaltr_humid}")

            hora_atual = dt.datetime.now()

            st_humid = hora_atual - horaltr_humid

            if st_humid > t10s:
                humid_media = dados_humid()
                horaltr_humid = dt.datetime.now()   ### atualiza a hr da leitura
                #print(f"{hora_atual} -- hora humid ")
                
                humid = (humid_media, hora_atual)
                db_humid(conn, humid)

                ativairrig = True

                conn.close()


            # **************    get humid temp do dht11       ***********************

            #humid, temp = dados_dht11(humid, temp)

            conn = create_connection(r"EstufaDB.db")

            horaltr_dht11 = get_data(conn, tb_dht11)
            horaltr_dht11 = datetime.strptime(horaltr_dht11, '%Y-%m-%d %H:%M:%S.%f')

            hora_atual = dt.datetime.now()

            st_dht11 = hora_atual - horaltr_dht11
            

            if st_dht11 > t30s:
                humid_dht11, temp = dados_dht11(humid_dht11, temp)
                horaltr_dht11 = dt.datetime.now() ### atualiza a hr da leitura
                print(hora_atual)
            elif humid_dht11 < 100
                now = dt.datetime.now()
                dht11 = (temp, humid_dht11, now)
                db_dht11(conn, dht11)
                
                ativacooler = True
            else:
                #print("else")
                pass
            
            conn.close()

            # ***************    get volume do reservatorio    *********************

            st_reserv = hora_atual - horaltr_reserv

            if st_reserv > t10s:
                reserv_dados = dados_reserv()
                horaltr_reserv = dt.datetime.now()   ### atualiza a hr da leitura
                print(hora_atual)

                lst_final_reserv.append(reserv_dados)

                qtd_dados_reserv= len(lst_final_reserv)

                if qtd_dados_reserv >= 5:
                    res_final_reserv = float(sum(lst_final_reserv) / qtd_dados_reserv)

                    print(f'resultado da media do reserv = {res_final_reserv} ')

                    lst_final_reserv.clear()
                    conn = create_connection(r"EstufaDB.db")

                    now = dt.datetime.now()
                    reserv = (res_final_reserv, now)
                    db_reserv(conn, reserv)

                else:
                    pass

            else:
                #print("else")
                pass

        #******************************************************#
        # ******************* ATUADORES ********************** #
        #******************************************************#


                    #*** ativar cooler ***#
            while ativacooler = True
                if temp > 25:
                    print("cooler ligado")
                    gpio.output(rele1, 0)
                else:
                    gpio.output(rele1, 1)
                    ativacooler = False


                    #*** ativar irrig ***#
            while ativairrig = True
                if humid_media < 20:
                    print("irrigação ligada")
                    pio.output(rele2, 0)
                else:
                    gpio.output(rele2, 1)
                    ativairrig = False

        else:
            print("Espera por conectividade (10 segundos)")
            time.sleep(10.0)

except KeyboardInterrupt:
	print("\nPrograma terminado pelo utilizador.")
finally:
	print("ok.")
print("Fim do programa.")
