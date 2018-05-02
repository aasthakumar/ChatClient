import zmq
import sys
from threading import Thread

client_name = sys.argv[1]

def sending():
    context = zmq.Context()
    sock = context.socket(zmq.REQ)
    sock.connect("tcp://127.0.0.1:5677")

    while 1:
        val = str("[" + client_name + "]:" + input("[" + client_name + "]>"))
        #print(val)
        sock.send_string(val)
        mess= (sock.recv().decode())

def receiving():
    context = zmq.Context()
    sock = context.socket(zmq.SUB)
    sock.setsockopt_string(zmq.SUBSCRIBE, "")
    sock.connect("tcp://127.0.0.1:5678")

    while True:
        message= sock.recv().decode()
        if message.find("[" + client_name + "]:") != 0:
            print("\n" + message + "\n[" + client_name + "]>", end="")
            

print("User[" + client_name + "] Connected to the chat server.")

output = (Thread(target=sending, args=( )))
output.start()

receive = (Thread(target=receiving, args=( )))
receive.start()
