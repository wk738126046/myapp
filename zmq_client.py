import zmq
import random
import sys, os
import time
import json
port = "5556"
context = zmq.Context()
import math

data = {}
# data['img_path'] = os.getcwd() + '/detector/detect_model/test_img/person.jpg'
data['img_path'] = '/home/wk/wk_ws/yolo_ws/mask_rcnn/images/test.jpg'
data['thresh'] = 0.5
now = time.time()
identity = str(random.randint(1,100000))
print(identity)
socket = context.socket(zmq.DEALER)
socket.identity = identity.encode('ascii')
socket.connect("tcp://127.0.0.1:%s" % port)

socket.send(json.dumps(data))
result = socket.recv()
# time.sleep(1)
print(time.time() - now)
print(result)
