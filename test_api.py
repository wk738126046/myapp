#!/usr/bin/python
import urllib
import urllib2
import requests
import sys
import json
import os
import time
HOST_IP = '127.0.0.1'
PORT = '8000'
def post(url, data, files = None):
    # req = urllib2.Request(url)
    # data = urllib.urlencode(data)

    response = requests.post(url, data = data, files = files)
    return response.content
def detect(url):
    posturl = "http://" + HOST_IP + ":" + "8000" + "/detector/api/detect"
    data = {"url": url}
    data = post(posturl, data)
    print(data)
    return json.loads(data)
def upload(path):
    data = {}
    posturl = "http://" + HOST_IP + ":" + "8000" + "/detector/api/upload"
    data = {"img": (os.path.split(path)[-1], open(path, 'rb')) }
    url = post(posturl,data = data, files = data)
    return url
def upload_and_detect(path):
    posturl = "http://" + HOST_IP + ":" + "8000" + "/detector/api/upload_and_detect"
    data = {"img": (os.path.split(path)[-1], open(path, 'rb')) }
    result = post(posturl,data = data, files = data)

    return result
if __name__ ==  "__main__":
    doc = """
        Usage: 
        python ./test_api.py detect image_url For example: test_api detect http://127.0.0.1:9000/0.jpg       
        python ./test_api.py upload image_path For example: test_api upload data/0.jpg 
        python ./test_api.py upload_and_detect image_path For example: test_api upload_and_detect data/0.jpg
        """
    if len(sys.argv) < 3:
        print(doc)
    else:
        if sys.argv[1] == 'detect':
            print(detect(sys.argv[2]))

        elif sys.argv[1] == 'upload':
            print(upload(sys.argv[2]))

        elif sys.argv[1] == 'upload_and_detect':
            print(upload_and_detect(sys.argv[2]))
        elif sys.argv[1] == 'multiprocess_test':
            import thread
            for i in range(2):
                thread.start_new_thread(detect, (sys.argv[2],))
        else:
            print("Error Usage.")
            print(doc)
        time.sleep(1)