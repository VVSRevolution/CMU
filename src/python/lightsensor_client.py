#from __future__ import print_function

import logging

import grpc
import iot_service_pb2
import iot_service_pb2_grpc

from const import *


def getluz():
    with grpc.insecure_channel(GRPC_SERVER+':'+GRPC_PORT) as channel:
        stub = iot_service_pb2_grpc.IoTServiceStub(channel)
        response = stub.SayLightLevel(iot_service_pb2.LightLevelRequest(sensorName='my_sensor'))

    print(f"\tLight level received:  {100 - int(response.lightLevel)}%")
    return 100 - int(response.lightLevel)

if __name__ == '__main__':
    logging.basicConfig()
    getluz()
