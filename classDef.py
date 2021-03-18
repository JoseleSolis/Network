class Device:
    def __init__(self, name,pNumber,id):
        self.id = id
        self.name = name
        self.states = ["null"]*pNumber
        self.ports = [None]*pNumber
        self.valueInChannel = -1
    def send(self):
        for i in range(len(self.ports)):
           for j in range(len(self.ports[i].ports)):
               if self.ports[i].ports[j] == self:
                   self.ports[i].states[j] = "receiving"
                   self.ports[i].valueInChannel = self.valueInChannel
               elif(self.ports[i].ports[j] is None): 
                   self.ports[i].states[j] = "null"
               else:
                   self.ports[i].states[j] = "sending"
                   self.ports[i].valueInChannel = self.valueInChannel
                   self.ports[i].ports[j].send()
            
class Hub(Device):
    def __init__(self, name, pNumber,id):
        super().__init__(name, pNumber,id)

 
class Host(Device):
    def __init__(self, name,id):
         super().__init__(name, 1,id)
         self.dataToSend = []
         self.collision = ' '
       

class Set():
    def __init__(self):
        self.Devices = []
        self.Visited = []
    
    def add(self,device):
        self.Devices.append([device])
    

    def mergeNetworks(self, device1, device2):
        device_one_list = self.listOf(device1)
        device_two_list = self.listOf(device2)
        for i in device_two_list:
            device_one_list.append(i)
        self.Devices.remove(device_two_list)
        
    def listOf(self, device):
        for i in self.Devices:
            for j in i:
                if j == device:
                    return i

    def divideNetwork(self,device1,device2):
        formerList = self.listOf(device1)
        device_one_list = []
        device_two_list = []
        
        self.Visited = [False]*len(formerList)
        self.DFS_visit(device1, formerList)
        for i in range(len(self.Visited)):
            if self.Visited[i]:
                device_one_list.append(formerList[i])
            else:
                device_two_list.append(formerList[i])
        
        self.Devices.remove(formerList)
        self.Devices.append(device_one_list)
        if(len(device_two_list)):
            self.Devices.append(device_two_list)
 
    def DFS_visit(self,device,formerList):
        self.Visited[formerList.index(device)] = True
        for i in device.ports:
            if i is not None and not self.Visited[i]:
                DFS_visit(i,formerList)
        



    