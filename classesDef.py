class Device:
    def __init__(self, name,pNumber,id):
        self.id = id
        self.name = name
        self.isSending = 0
        self.bitToSend = 0
        self.ports = [None]*pNumber
    #def networkOf(self):
    #    if(father[self.id] != self.id):
    #        father[self.id] = devices[father[self.id]].networkOf()
    #    return father[self.id]
    #def merge(self,x):
    #    selfR = self.networkOf()
    #    xR = x.networkOf()
    #    if(selfR == xR):
    #        return
    #    if(rank[selfR] < rank[xR]):
    #        father[selfR] = xR
    #    elif(rank[selfR] > rank[xR]):
    #        father[xR] = selfR
    #    else:
    #        father[xR] = selfR
    #        rank[selfR] +=1
class Hub(Device):
    def __init__(self, name, pNumber,id):
        super().__init__(name, pNumber,id)

class Host(Device):
    def __init__(self, name,id):
         super().__init__(name, 1,id)


class Set():
    def __init__(self):
        self.Devices = []
        self.Father = []
        self.Rank = []

    def add(self,device):
        self.Devices.append(device)
        self.Father.append(device.id)
        self.Rank.append(0)

    def networkOf(self,x):
        if(self.Father[x.id] != x.id):
            self.Father[x.id] = self.networkOf(self.Devices[self.Father[x.id]])
        return self.Father[x.id]
   
    def mergeNetwork(self,y,x):
        yR = self.networkOf(y)
        xR = self.networkOf(x)
        if(yR == xR):
            return
        if(self.Rank[yR] < self.Rank[xR]):
            self.Father[yR] = xR
        elif(self.Rank[yR] > self.Rank[xR]):
            self.Father[xR] = yR
        else:
            self.Father[xR] = yR
            self.Rank[yR] +=1
    


