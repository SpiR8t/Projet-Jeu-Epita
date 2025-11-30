import asyncio, json, requests,time, threading
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCConfiguration, RTCIceServer
from random import *
from queue import Queue

def start_network(is_host):
    if is_host:
        start_host()
    else:
        start_client()

def start_host():
    pass

def start_client():
    pass