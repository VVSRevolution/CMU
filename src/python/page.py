from flask import *
from db import *
from thermometer_client import *
from lightsensor_client import *
from led_client import *
import logging, threading, time
import sys
from datetime import datetime
import math
import grpc
import iot_service_pb2, iot_service_pb2_grpc


GRPC_SERVER = '3.89.99.208'
GRPC_PORT = '50051'

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
        if 'dateTime' in json:
            condicional += "Data "

            # Converter a string para um objeto datetime
            data_hora_obj = datetime.strptime(json['dateTime'], "%Y-%m-%dT%H:%M")

            # Formatar a data e hora no formato desejado
            data_hora_formatada = data_hora_obj.strftime("%d/%m/%Y %H:%M")

            condicional += data_hora_formatada


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


@app.route("/delete_rotine/<int:rotine_id>")
def delete_rotine(rotine_id):

    resources = rotinas.get(rotinas.id == rotine_id)
    try:
        resources.delete_instance()
        print("Item with ID", rotine_id, "deleted successfully.")

    except resources.DoesNotExist:
        print("Item with ID", rotine_id, "not found.")

    return redirect(url_for('rotines'))    

@app.route("/rotines",methods =['GET', 'POST'])
def rotines():
    if request.method == 'GET':
        headers = ("ID","Condicional","Estado")
        resources = rotinas.select()
        try:
            print("\033[1m[ROTINE]:\033[0m\tConsultando Rotinas")
            
        except:
            print("\033[1m[ROTINE]:\033[0m\tERRO no processo de consulta do Rotinas")
        else:
            return render_template("rotinas.html",headings=headers, data=resources)
    if request.method == 'POST':
        id = request.form.get('id')
        print(id)
        return redirect(url_for('delete_rotine', rotine_id = id)) 
    
def checkCondicionalData(Data, estado):
    data_hora_obj = datetime.strptime(Data, "%d/%m/%Y %H:%M")
    data_hora_atual = datetime.now()
    if data_hora_obj == data_hora_atual:

def checkCondicionalTemperatura(num, cond, comp, estado):
    atuador, cor, status = estado

    status = mudaStatus(status)
    cor = mudaCor(cor)
    print(f"\n[BY TEMP]")
    print(f"\tAtuador:" + atuador)
    print(f"\tCor: " + cor)
    print(f"\tStatus: " + str(status))

    if(cond == ">"):
        if (num > int(comp)):
            if(atuador == "luz"):
                setluz(int(status),cor)
                
    elif(cond == ">="):
        if (num >= int(comp)):
            if(atuador == "luz"):
                setluz(int(status),cor)
                
    elif(cond == "<="):
        if (num <= int(comp)):
            if(atuador == "luz"):
                setluz(int(status),cor)
                
    elif(cond == "="):
        if (num == int(comp)):
            if(atuador == "luz"):
                setluz(int(status),cor)
                

    elif(cond == "<"):
        if (num < int(comp)):
            if(atuador == "luz"):
                setluz(int(status),cor)


def mudaStatus(status):
    return 0 if status == "Desligada" else 1

def mudaCor(cor):
    return "green" if cor == "verde" else "red"

def checkCondicionalLuminosidade(num, cond, comp, estado):
    atuador, cor, status = estado
    status = mudaStatus(status)
    cor = mudaCor(cor)
    print(f"\n[BY TEMP]")
    print(f"\tAtuador:" + atuador)
    print(f"\tCor: " + cor)
    print(f"\tStatus: " + str(status))

    if(cond == ">"):
        if (num > int(comp)):
            if(atuador == "luz"):
                setluz(int(status),cor)
                
    elif(cond == ">="):
        if (num >= int(comp)):
            if(atuador == "luz"):
                setluz(int(status),cor)
                
    elif(cond == "<="):
        if (num <= int(comp)):
            if(atuador == "luz"):
                setluz(int(status),cor)
                
    elif(cond == "="):
        if (num == int(comp)):
            if(atuador == "luz"):
                setluz(int(status),cor)
                

    elif(cond == "<"):
        if (num < int(comp)):
            if(atuador == "luz"):
                setluz(int(status),cor)

def splitString(string):
    return string.split(sep=" ")


def checkrotines():
    print("checkrotines called")
    time.sleep(0.5)
    while(True):
        querry = rotinas.select()
        for i in querry:
            print(f"\n[ROTINE]\t{i.condicao} --> {i.estado}")
            condicao = i.condicao.split(" ")
            estado = i.estado.split(" ")
            print(f"\n[STATUS]")
            temp = gettemperatura()
            light = getluz()


            if condicao[0] == "temperatura":
                checkCondicionalTemperatura(float(temp), condicao[1], condicao[2], estado)
            if condicao[0] == "luminosidade":
                checkCondicionalLuminosidade(light, condicao[1], condicao[2], estado)
            if condicao[0] == "Data":
                checkCondicionalData(f"{condicao[1]} {condicao[2]}",estado)
        
            time.sleep(2)


def setup():
    global GRPC_SERVER, GRPC_PORT
    GRPC_SERVER = input("\033[1m[SET UP]:\033[0m\t\tEntre com GRPC IP: ")
    GRPC_PORT = input("\033[1m[SET UP]:\033[0m\t\tEntre com GRPC PORT: ")




if __name__ == "__main__":
    logging.basicConfig()
    #setup()
    check = threading.Thread(target=checkrotines)
    check.start()
    app.run(debug=True,  use_reloader=False, port=8080)