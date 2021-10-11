import string
import random
import hashlib

def randomString(size =20):
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.choice(chars)for _ in range(size))

def randomName(n=30):
    s = randomString(n)
    hash_object = hashlib.sha1(s.encode())
    name = hash_object.hexdigest()
    nameAsNum=int(name,16)
    return nameAsNum

def sha1Serv(serverName):
    hash_object = hashlib.sha1(serverName.encode())
    name = hash_object.hexdigest()
    nameAsNum=int(name,16)
    return nameAsNum

def aEntero(s):
    hash_object = hashlib.sha1(s)
    name = hash_object.hexdigest()
    nameAsNum=int(name,16)
    return nameAsNum

class Range:
    def __init__(self,lb,ub):
        self.lb = lb            # 0 - 10 -  20 - 30 
        self.ub = ub
    
    def isFirst(self):
        return self.lb > self.ub
    
    def member(self, id):
        if self.isFirst():
            return (id >= self.lb and id < 1<<160) or (id >= 0 and id < self.ub )
        else:
            return id >= self.lb and id < self.ub
    
    def toStr(self):
        if self.isFirst():
            return '[' + str(self.lb) + ' , 2^160) U [' + '0 , ' +  str(self.ub) + ')'
        else:
            return '[' + str (self.lb) + ' , ' + str(self.ub) + ')'


""" servers = [randomName() for _ in range(5)]
servers.sort()
ranges = []
for n in range(len(servers)-1):
    lb = servers[n]
    ub = servers[n+1]
    ranges.append(Range(lb,ub))
ranges.append(Range(servers[4], servers[0]))

load = {}
Files = 10
file = 'imagen3.jpg'
index = file.split('.')[0]+'.index'

with open(file, 'rb') as f:
    with open(index, 'a') as f2:
        f2.write(file+'\n')
        while True:
            aux = f.read(1024*100)
            if (not len(aux)):
                break
            hf = aEntero(aux)
            
            for s in ranges:
                if s.member(hf):
                    print('nelson estoyn aca..')
                    f2.write(str(hf)+'\n')
                    break """
            


