import classesDef as myClass

idCount = 0

mySet = myClass.Set()
#devices = []
#father = []
#rank = []

def main():
    f = open('script.txt','r') 
    lines = [line.split() for line in f]
    f.close()
    time = 0
    while(len(lines)):
       if(int(lines[0][0]) == time):
           instruction = lines.pop(0)
           if(instruction[1] == "create"):
               create(instruction)
           elif(instruction[1] == "connect"):
               connect(instruction)
           elif(instruction[1] == "disconnect"):
               disconnect(instruction)
           else:
               send(instruction)
       else:
           time+=1    
    print(mySet.Father)
def create(instruction):
    #global devices
    global idCount
    if(instruction[2] == "host"):
        mySet.add(myClass.Host(instruction[3],idCount))
        #devices.append(myClass.Host(instruction[3],idCount))
    else:
        mySet.add(myClass.Hub(instruction[3],int(instruction[4]),idCount))
        #devices.append(myClass.Hub(instruction[3],int(instruction[4]),idCount))

    #father.append(idCount)
    #rank.append(0)
    idCount+=1
    return
def connect(instruction):
    #global devices
    port_1 = instruction[2].split('_')
    port_2 = instruction[3].split('_')
    device_1 = None
    device_2 = None
    for i in mySet.Devices:
    #for i in devices:
        if(i.name == port_1[0]):
            device_1 = i
        elif(i.name == port_2[0]):
            device_2 = i
    device_1.ports[int(port_1[1])-1] = device_2
    device_2.ports[int(port_2[1])-1] = device_1
    mySet.mergeNetwork(device_1,device_2)
    #device_1.merge(device_2)
    return
def disconnect(instruction):
    #global devices
    #global father
    #global rank
    port = instruction[2].split('_')
    for i in mySet.Devices:
    #for i in devices:
        if(i.name == port[0]):
            otherEnd = i.ports[int(port[1])-1].name
            disconnectOtherEnd(otherEnd, i.name)    #cuando desconecto un cable se desconectan dos dispositivos, este metodo es para desconectar el primer dispositivo del puerto en q se encuentre en el segundo dispositivo
            i.ports[int(port[1])-1] = None
            break
    mySet.Father = [x for x in range(len(mySet.Devices))]
    mySet.Rank = [0]*len(mySet.Devices)
    #father = [x for x in range(len(devices))]
    #rank = [0]*len(devices)
    DFS()
    return
def disconnectOtherEnd(otherEndName, deviceToDisconnect):
    #global devices
    for i in mySet.Devices:
    #for i in devices:
        if(i.name == otherEndName):
            for j in range(len(i.ports)):
                if(i.ports[j].name == deviceToDisconnect):
                    i.ports[j] = None
                    return
    return
def DFS():
    visited = [False]*len(mySet.Father)
    #visited = [False]*len(father)
    for i in mySet.Devices:
    #for i in devices:
        if not visited[i.id]:
            DFS_Visit(visited,i)
def DFS_Visit(visited,v):
    visited[v.id] = True
    for i in v.ports:
        if i is not None and not visited[i.id]:
            mySet.mergeNetwork(v,i)
            #v.merge(i)
            DFS_Visit(visited,i)



#class Device:
#    def __init__(self, name,pNumber):
#        self.id = idCount
#        self.name = name
#        self.isSending = 0
#        self.bitToSend = 0
#        self.ports = [None]*pNumber
#    def networkOf(self):
#        if(father[self.id] != self.id):
#            father[self.id] = devices[father[self.id]].networkOf()
#        return father[self.id]
#    def merge(self,x):
#        selfR = self.networkOf()
#        xR = x.networkOf()
#        if(selfR == xR):
#            return
#        if(rank[selfR] < rank[xR]):
#            father[selfR] = xR
#        elif(rank[selfR] > rank[xR]):
#            father[xR] = selfR
#        else:
#            father[xR] = selfR
#            rank[selfR] +=1
#class Hub(Device):
#    def __init__(self, name, pNumber):
#        super().__init__(name, pNumber)
#
#class Host(Device):
#    def __init__(self, name):
#         super().__init__(name, 1)
#

main()



