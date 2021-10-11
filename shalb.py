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

class Range:
    def __init__(self,lb,ub):
        self.lb = lb
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

servers = [randomName() for _ in range(5)]
servers.sort()
ranges = []
for n in range(len(servers)-1):
    lb = servers[n]
    ub = servers[n+1]
    ranges.append(Range(lb,ub))
ranges.append(Range(servers[4], servers[0]))

load = {}
Files = 10
for r in range(Files):
    fileId = randomName()
    for s in ranges:
        if s.member(fileId):
            cl = load.get(s.toStr(),0)
            load[s.toStr()]= cl + 1
            break

for key in load.keys():
    print("{} -> {}".format(key, load[key] / Files))