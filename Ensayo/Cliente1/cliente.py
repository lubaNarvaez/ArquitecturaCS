import zmq
import sys
import json
import time
from shalb import sha1Serv, Range, aEntero

SIZE = 1048576

params = {
    'user': sys.argv[1],
    'opcion': sys.argv[2],
    'file': sys.argv[3] if sys.argv[2] != 'list' else 0
}


serverNames = ['serv1', 'serv2', 'serv3', 'serv4', 'serv5']

serverSha = []

serverSocket ={}

servers = []

for socket in range(1,6):
    context = zmq.Context()
    s = context.socket(zmq.REQ)
    s.connect('tcp://localhost:800{}'.format(socket))
    servers.append(s)

for item in range(5):
    sha_one = sha1Serv(serverNames[item])
    serverSha.append( sha_one )
    serverSocket[sha_one] = servers[item]
     

print(serverSha)

print('-------------------------------------------')




serverSha.sort()
print(serverSha)
ranges = []

for n in range(len(serverSha)-1):
    lb = serverSha[n]
    ub = serverSha[n+1]
    ranges.append(Range(lb,ub))
ranges.append(Range(serverSha[4], serverSha[0]))

print('+++++++++++++++')

for item in ranges:
    print(item.toStr())

print('**********************************')

print(serverSocket)


if(params.get('opcion') == 'upload'):

    index = params.get('file').split('.')[0]
    index = index+'.index'

    with open(params.get('file'), 'rb') as f:
        with open(index, 'a') as f2:

            f2.write(params.get('file')+'\n')
            Mbyte = f.read(SIZE)
            while True:
                
                if (not len(Mbyte)):
                    break
                hf = aEntero(Mbyte)

                for s in ranges:
                    if s.member(hf):        
                        socket = serverSocket.get(s.lb)
         
                        print('limite inferior: '+str(s.lb)+'    limite superior:  '+str(s.ub)+  '\n ----> '+str( hf)+ 'al socket: '+str(socket.get_monitor_socket())+'\n')
                        f2.write(str(hf)+'\n')
                        data = json.dumps(params)
                        socket.send_string(data)
                        socket.recv_string()
                        socket.send_multipart([Mbyte])
                        socket.recv_string()
                        Mbyte = f.read(SIZE)
                        time.sleep(1)
                        break 


            
elif (params.get('opcion') == 'download'):
    with open(params.get('file'), 'ab') as f:
        while True:
            data = json.dumps(params)
            s.send_string(data)
            byte = s.recv_multipart()
            if len(byte[0])==0:
                break
            f.write(byte[0])

elif (params.get('opcion') == 'list'):
    data = json.dumps(params)
    s.send_string(data)
    listFiles = s.recv_string()
    print(listFiles)

elif (params.get('opcion') == 'sharelink'):
    data = json.dumps(params)
    s.send_string(data)
    link = s.recv_string()
    print(link)
    
elif (params.get('opcion') == 'downloadlink'):
    data = json.dumps(params)
    s.send_string(data)
    data = s.recv_string()
    params = json.loads(data)
    params['opcion'] = 'download'
    with open(params.get('file'), 'ab') as f:
        while True:
            data = json.dumps(params)
            s.send_string(data)
            byte = s.recv_multipart()
            if len(byte[0])==0:
                break
            f.write(byte[0])


    
# python cliente.py username upload file.ext