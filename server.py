import zmq
import time
from threading import Thread
from queue import Queue


def client_msg_receive(q):
    context = zmq.Context()
    sock = context.socket(zmq.REP)
    sock.bind("tcp://127.0.0.1:5677")
    while True:
        message = str(sock.recv().decode())
        sock.send_string("Echo: " + message)
        q.put(message)

def client_msg_broadcast(q):
    context = zmq.Context()
    sock = context.socket(zmq.PUB)
    sock.bind("tcp://127.0.0.1:5678")
    while True:
        while q.qsize() != 0:
            current_message = q.get()
            sock.send_string(current_message)
            q.task_done()

q = Queue(maxsize=0)

input = (Thread(target=client_msg_receive, args=(q, )))
input.start()

broadcast = (Thread(target=client_msg_broadcast, args=(q, )))
broadcast.start()
