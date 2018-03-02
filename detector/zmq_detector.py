import zmq
import random
import sys, os
import time
import json
import math
from django.conf import settings
class ZmqDetector():
    def __init__(self, port = "5556"):
        self.port = port
        self.context = zmq.Context()
    def detect(self, path, id, thresh = 0.5):
        data = {}
        data['img_path'] = path
        data['thresh'] = thresh
        identity = id
        print(identity)
        socket = self.context.socket(zmq.DEALER)
        socket.identity = identity.encode('ascii')
        socket.connect("tcp://%s:%s" % (settings.DETECTOR_HOST, self.port))
        socket.send(json.dumps(data))
        result = socket.recv()
        return result
