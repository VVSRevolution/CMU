from flask import *
from db import *
import logging, threading, time
import sys

import grpc
#import iot_service_pb2, iot_service_pb2_grpc


GRPC_SERVER = ""
GRPC_PORT = ""

app = Flask(__name__)

@app.route("/",methods =['GET', 'POST'])
def home():

    if request.method == 'GET':

        try:
            print("[MANAGER_HIGH]:\tConsultando Resources em /sons")
            resources = rotinas.select()
        except:
            print("[MANAGER_HIGH]:\tERRO no processo de consulta do Resource em /sons")
        
    if request.method == 'POST':

        json = request.json

        print(json)

        try:
            print("[MANAGER_HIGH]:\tConsultando Resources em /sons")
            resources = rotinas.select()
        except:
            print("[MANAGER_HIGH]:\tERRO no processo de consulta do Resource em /sons")
        
        condicional = ''

        if 'condition' in json:
            condicional += json['optionSelect'] 
            if(json['condition'] == "menor"): condicional += " < "
            if(json['condition'] == "menorigual"): condicional += " <= "
            if(json['condition'] == "igual"): condicional += " = "
            if(json['condition'] == "maiorr"): condicional += " > "
            if(json['condition'] == "maiorigual"): condicional += " < "
            if json['optionSelect'] == "luminosidade": condicional += json['luminosidade']
            if json['optionSelect'] == "temperatura": condicional += json['temperatura']
        if 'dataTime' in json:
            condicional += "Data"
            if(json['dataTime']):  condicional += json['dataTime']

        entao = ''
        entao += json['execute']
        entao += ' '
        entao += json['lightColor']
        if json['luzLigadoDesligadoCheckbox'] == True: entao += " Ligada"
        else: entao += " Desligada"

        query = rotinas.create(
            condicao=condicional,
            estado=entao
        )

    return render_template("table_enviar.html")

def delete_rotina(id):
    # Implemente a lógica para excluir do banco de dados aqui
    pass    

@app.route("/delete_rotine/<int:rotine_id>", methods=['POST'])
def delete_rotine(rotine_id):
    delete_rotina(rotine_id)
    return redirect(url_for('rotines'))    

@app.route("/rotines",methods =['GET', 'POST'])
def rotines():
    if request.method == 'GET':
        headers = ("ID","Condicional","Estado")
        try:
            print("\033[1m[ROTINE]:\033[0m\tConsultando Rotinas")
            resources = rotinas.select()
        except:
            print("\033[1m[ROTINE]:\033[0m\tERRO no processo de consulta do Rotinas")
        else:
            return render_template("rotinas.html",headings=headers, data=resources)
    if request.method == 'POST':
        id = request.form.get('id')
        print(id)
        return "teste"

def checkrotines():
    querry = rotinas.select()
    for i in querry:
        print(i.condicao)
    
    time.sleep(2)

def setup():
    global GRPC_SERVER, GRPC_PORT
    GRPC_SERVER = input("\033[1m[SET UP]:\033[0m\t\tEntre com GRPC IP: ")
    GRPC_PORT = input("\033[1m[SET UP]:\033[0m\t\tEntre com GRPC PORT: ")


def ligar_luz(luz ,estado):
    global GRPC_SERVER, GRPC_PORT
    with grpc.insecure_channel(GRPC_SERVER+':'+GRPC_PORT) as channel:
        stub = iot_service_pb2_grpc.IoTServiceStub (channel)
        response = stub.BlinkLed(iot_service_pb2.LedRequest(state=int(estado),ledname=luz))

    if response.ledstate[sys.argv[2]] == 1:
        print("Led state is on")
    else:
        print("Led state is off")

def lightsensor():
    global GRPC_SERVER, GRPC_PORT
    with grpc.insecure_channel(GRPC_SERVER+':'+GRPC_PORT) as channel:
        stub = iot_service_pb2_grpc.IoTServiceStub(channel)
        response = stub.SayLightLevel(iot_service_pb2.LightLevelRequest(sensorName='my_sensor'))

    print("Light level received: " + response.lightLevel)
    return response.lightLevel

def thermometer():
    with grpc.insecure_channel(GRPC_SERVER+':'+GRPC_PORT) as channel:
        stub = iot_service_pb2_grpc.IoTServiceStub(channel)
        response = stub.SayTemperature(iot_service_pb2.TemperatureRequest(sensorName='my_sensor'))

    print("Temperature received: " + response.temperature)
    return response.temperature

if __name__ == "__main__":
    logging.basicConfig()
    setup()
    check = threading.Thread(target=checkrotines)
    check.start()
    app.run(debug=True,  use_reloader=False, port=12345)