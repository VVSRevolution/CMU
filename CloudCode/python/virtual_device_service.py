from kafka import KafkaConsumer, KafkaProducer
from const import *
import threading

from concurrent import futures
import logging

import grpc
import iot_service_pb2
import iot_service_pb2_grpc
import ssl

# Twin state
current_temperature = 'void'
current_light_level = 'void'
led_state = {'red':0, 'green':0}
username = "admin"
password = "admin-secret"

seguranca = False #ativar segurança

# Kafka consumer to run on a separate thread
def consume_temperature():
    global current_temperature
    if seguranca:
        consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER+':'+KAFKA_PORT,
                                security_protocol='SASL_PLAINTEXT',
                                sasl_mechanism='PLAIN',
                                sasl_plain_username=username,
                                sasl_plain_password=password)
    else:
        consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER+':'+KAFKA_PORT)
    consumer.subscribe(topics=('temperature'))
    for msg in consumer:
        print ('Received Temperature: ', msg.value.decode())
        current_temperature = msg.value.decode()

# Kafka consumer to run on a separate thread
def consume_light_level():
    global current_light_level
    if seguranca:
        consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER+':'+KAFKA_PORT,
                                security_protocol='SASL_PLAINTEXT',
                                sasl_mechanism='PLAIN',
                                sasl_plain_username=username,
                                sasl_plain_password=password)
    else:
        consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER+':'+KAFKA_PORT)
    consumer.subscribe(topics=('lightlevel'))
    for msg in consumer:
        print ('Received Light Level: ', msg.value.decode())
        current_light_level = msg.value.decode()

def produce_led_command(state, ledname):
    if seguranca:
         consumer = KafkaProducer(bootstrap_servers=KAFKA_SERVER+':'+KAFKA_PORT,
                                security_protocol='SASL_PLAINTEXT',
                                sasl_mechanism='PLAIN',
                                sasl_plain_username=username,
                                sasl_plain_password=password)
    else:
        producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER+':'+KAFKA_PORT)
    producer.send('ledcommand', key=ledname.encode(), value=str(state).encode())
    return state
        
class IoTServer(iot_service_pb2_grpc.IoTServiceServicer):

    def SayTemperature(self, request, context):
        return iot_service_pb2.TemperatureReply(temperature=current_temperature)
    
    def BlinkLed(self, request, context):
        if(request.login == "adm" and request.senha == "123"):
            print ("Blink led ", request.ledname)
            print ("...with state ", request.state)
            produce_led_command(request.state, request.ledname)
            # Update led state of twin
            led_state[request.ledname] = request.state
            return iot_service_pb2.LedReply(ledstate=led_state)
        else: 
            return iot_service_pb2.LedReply(ledstate=led_state)

    def SayLightLevel(self, request, context):
        return iot_service_pb2.LightLevelReply(lightLevel=current_light_level)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    iot_service_pb2_grpc.add_IoTServiceServicer_to_server(IoTServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()

    trd1 = threading.Thread(target=consume_temperature)
    trd1.start()

    trd2 = threading.Thread(target=consume_light_level)
    trd2.start()

    # Initialize the state of the leds on the actual device
    for color in led_state.keys():
        produce_led_command (led_state[color], color)
    serve()
