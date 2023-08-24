#from __future__ import print_function

import logging
import sys

import grpc
import iot_service_pb2
import iot_service_pb2_grpc


from const import *


def setluz(estado, cor):
    with grpc.insecure_channel(GRPC_SERVER+':'+GRPC_PORT) as channel:
        stub = iot_service_pb2_grpc.IoTServiceStub (channel)
        response = stub.BlinkLed(iot_service_pb2.LedRequest(state=int(estado),ledname=cor))

    if response.ledstate[sys.argv[2]] == 1:
        print("Led state is on")
    else:
        print("Led state is off")

if __name__ == '__main__':
    logging.basicConfig()
    setluz()
