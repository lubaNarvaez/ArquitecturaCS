import zmq      # Provee la comunocación a través de sockets
import sys

SIZE = 1048576
context = zmq.Context()



# Crea un socket y lo conecta a tarvés del protocolo 
# tcp con el equipo local en el puerto 8001
s= context.socket(zmq.REQ)
s.connect('tcp://localhost:8001')

user = sys.argv[1]
op = sys.argv[2]

if (op != 'list'):
    file = sys.argv[3]



if (op == "upload"):
    
    with open (file, 'rb') as f:
        Mb = f.read(SIZE)
        while True:
            if not Mb:
                break
            s.send_string(op)
            s.recv_string()
            s.send_string(user)
            s.recv_string()
            s.send_string(file)
            s.recv_string()
            s.send_multipart([Mb])
            s.recv_string()
            Mb = f.read(SIZE)
        

elif(op  == 'download'):
    with open(file, 'ab') as f:
        while True:
            s.send_string(op)
            s.recv_string()
            s.send_string(user)
            s.recv_string()
            s.send_string(file)
            byte = s.recv_multipart()
            if len(byte[0]) == 0:
                break
            f.write(byte[0])

elif(op == 'list'):
    s.send_string(op)
    s.recv_string()
    s.send_string(user)
    arc = s.recv_string()
    print (arc)

elif(op  == 'sharelink'):
    s.send_string(op)
    s.recv_string()
    s.send_string(user)
    s.recv_string()
    s.send_string(file)
    link = s.recv_string()
    print (link)

elif(op  == 'downloadlink'):
    s.send_string(op)
    s.recv_string()
    s.send_string(user)
    s.recv_string()
    s.send_string(file)
    nombre = s.recv_string()
    s.send_string('ok')
    with open(nombre, 'wb') as f:
        byte = s.recv_multipart()
        f.write(byte[0])