
temperature_topic = "t0th/temperature"
humidity_topic = "t0th/humidity"
broker_url = "127.0.0.1"
bkrMqtt = None

cont_sensors_humid = ["1","2"]  # variavel que contem a quantidade de sensores ligados ao arduino
resultado_humidade = []
lst_final_humid = []
res_final_humid = None
tb_humid = "humid"
tb_dht11 = "dht11"
hora_atual = None
humid_media = None
lidoard = None
msg = None
msgr = None
humid = None
temp = None
hora1 = None