from types import SimpleNamespace
import zmq
import os
import hashlib
import json

# BUF_SIZE is totally arbitrary, change for your app!
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
SIZE = 1048576
users = {}
context = zmq.Context()
s = context.socket(zmq.REP)
s.bind('tcp://*:8001')

while True:
    op= s.recv_string()
    s.send_string('ok')
    if(op=='upload'):
        user = s.recv_string()
        s.send_string('ok')
        file = s.recv_string()
        s.send_string('ok')
        with open(file, 'ab') as f:
            Mb = s.recv_multipart()
            f.write(Mb[0])
            s.send_string('ok')

    elif(op  == 'download'):
        user = s.recv_string()
        s.send_string('ok')
        file = s.recv_string()
        contador =open (file, 'rb')
        if users.get(user)==None:
            users[user] = 0
        pos = users[user]
        contador.seek(pos)
        byte = contador.read(SIZE)
        users[user]= contador.tell()
        s.send_multipart([byte])

    elif(op  == 'list'):
        user = s.recv_string()
        arc = os.listdir('.')
        cont = '\n'.join(arc)    
        s.send_string(cont)

    elif(op  == 'sharelink'):
        user = s.recv_string()
        s.send_string('ok')
        file = s.recv_string()
        md5 = hashlib.md5()
        with open (file, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)
            link = md5.hexdigest()
            s.send_string(link)

    elif(op  == 'downloadlink'):
        user = s.recv_string()
        s.send_string('ok')
        link = s.recv_string()
        arcs = os.listdir('.')
        for arc in arcs:
            md5 = hashlib.md5()
            with open (arc, 'rb') as f:
                while True:
                    data = f.read(BUF_SIZE)
                    if not data:
                        break
                    md5.update(data)
            if link == md5.hexdigest():
                s.send_string(arc)
                break
                
                
    
    
