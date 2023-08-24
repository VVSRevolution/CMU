#from __future__ import print_function

import logging

import grpc
import iot_service_pb2
import iot_service_pb2_grpc

from const import *


def gettemperatura():
    with grpc.insecure_channel(GRPC_SERVER+':'+GRPC_PORT) as channel:
        stub = iot_service_pb2_grpc.IoTServiceStub(channel)
        response = stub.SayTemperature(iot_service_pb2.TemperatureRequest(sensorName='my_sensor'))

    print(f"\tTemperature received: {response.temperature}ºC")
    return response.temperature


if __name__ == '__main__':
    logging.basicConfig()
    runt()
