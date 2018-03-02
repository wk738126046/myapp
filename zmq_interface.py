#coding: utf-8
'''
yolo2 demo 文件放置在cnn工程下
本文件实现了与yoloapp兼容的zmq通信协议服务器。跨进程通信时zmq的延时只有1ms，在可接受范围之内。
客户端每次会向服务器发送一个请求，包含图片和客户端id。
服务器收到后将请求图片的地址放入队列，每次取出MAX_BATCH_SIZE张图片送入检测器进行处理。检测完成后向每个客户端返回识别结果。
检测器与zmq接收位于两个线程中。zmq使用了ROUTER/DELEAR方式，这样服务器能够识别出具体发送消息的客户端并选择性返回。
这样做的好处是可以充分利用显存和GPU的运算能力，降低用户的时延。
当然，服务器上的并行化处理对客户端透明，客户端所做的事情只是将请求发过来后再接收返回值，因此服务器的实现不局限于本代码的方法。
但是数据协议一定要按照本代码来。即客户端发送一个序列化的json，包含'img_path'和'thresh'两个值。返回结果为一个多级列表。端口为5556。
/detector/api/detect	POST	{"url":picture_url}	[ ["类别", 置信度, [中心点x坐标, 中心点y坐标, w, h] ],...]	url必须为通过uploadImg获得的图片url

'''
import zmq, json
import threading

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.ROUTER)
socket.bind("tcp://*:%s" % port)
task_queue = []
lock = threading.Lock()
MAX_BATCH_SIZE = 1

class DetectThread(threading.Thread):
    def __init__(self):

        super(DetectThread, self).__init__()

    def run(self):
        import darknet as dn
        dn.set_gpu(0)
        net = dn.load_net("cfg/yolo.cfg", "yolo.weights", 0)
        meta = dn.load_meta("cfg/coco.data")
        # r = dn.detect(net, meta, "data/bedroom.jpg")
        while True:
            global task_queue

            if len(task_queue) != 0:
                with lock:
                    if len(task_queue) >= MAX_BATCH_SIZE:
                        new_batch = task_queue[:MAX_BATCH_SIZE]
                        task_queue = task_queue[MAX_BATCH_SIZE:]
                    else:
                        new_batch = task_queue
                        for i in range(MAX_BATCH_SIZE - len(task_queue)):
                            new_batch.append(new_batch[0]) # maskRCNN要求图片数量与BATCH_SIZE相等，不足时使用第一张图片填充
                        task_queue = []
                identities = [item[0] for item in new_batch]
                msgs = [item[1] for item in new_batch]

                '''
                多张图片处理
                '''
                msgs = [json.loads(msg) for msg in msgs]
                img_paths = [msg['img_path'] for msg in msgs]
                results = []
                for img_path in img_paths:
                    result = dn.detect(net, meta, img_path)
                    results.append(result)

                for i, identity in enumerate(identities):
                    result = results[i]
                    socket.send_multipart([identity, json.dumps(result)])

if __name__ == '__main__':

    '''
    开启新线程
    '''
    t = DetectThread()
    t.start()

    '''
    循环等待数据
    '''
    while True:
        identity, msg = socket.recv_multipart()
        with lock:
            task_queue.append((identity, msg))
        print(identity, msg)
