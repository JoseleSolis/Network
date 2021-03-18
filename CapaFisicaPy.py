import classDef as myClass
from random import randint 
idCount = 0
mySet = myClass.Set() 


sendDevices = []

def main():
        
    signalTime = 3
    sending = []
    chosenSender = None

    f = open('script.txt','r') 
    lines = [line.split() for line in f]
    f.close()
    time = 0
    while(len(lines) or len(sendDevices)):
       while(len(lines) and int(lines[0][0]) == time):
           instruction = lines.pop(0)
           if(instruction[1] == "create"):
               create(instruction)
           elif(instruction[1] == "connect"):
               connect(instruction)
           elif(instruction[1] == "disconnect"):
               disconnect(instruction)
           else:
               send(instruction)
       
       

       if(len(sendDevices)):
         
           tempVisited = [False]*len(sendDevices)
           tempList = []
           for i in range(len(sendDevices)):    # el segundo for encuentra los dispositivos q quieren enviar y estan en la misma subred del i-esimo dispositivo escogido en el primer for
               if not tempVisited[i] and not sending.count(sendDevices[i]):                                                         
                   tempList.append(sendDevices[i])
                   iNetwork = mySet.listOf(sendDevices[i])
                    #si este dispositivo se encuentra en la red de otro elegido previamente a enviar, entonces este no puede enviar
                   mustContinue = False
                   for device in sending:
                       if iNetwork.count(device):    
                           mustContinue = True
                           break
                   if mustContinue:
                        continue                           

                   tempVisited[i] = True
                   for j in range(len(sendDevices)):
                       if not tempVisited[j] and iNetwork.count(sendDevices[j]):
                           tempList.append(sendDevices[j])
                    
                    #elegir un dispositivo aleatorio a enviar por cada subred
                   chosenSender = tempList[randint(0,len(tempList)-1)]
                   chosenSender.states[0] = 'sending'
                   chosenSender.valueInChannel = int(chosenSender.dataToSend.pop(0))
                   chosenSender.collision = 'ok' if len(tempList)==1 else 'collision'
                   chosenSender.timeSending = signalTime
                   
                   sending.append(chosenSender)
          
           for device in sending:   #cuando se llega a este punto todos los q pertenecen a sending son los que tienen q enviar
               device.timeSending -= 1
               device.send()
               if device.timeSending == 0:
                   sending.remove(device)    
                   if len(device.dataToSend) == 0:
                       sendDevices.remove(device) 
                       dfs_disconnect(device)
        
       for subNetwork in mySet.Devices:
           for device in subNetwork:
               s = open(device.name+'.txt','a+')
               for i in range(len(device.ports)):
                   if isinstance(device,myClass.Host):
                       print(str(time)+'  '+ device.name +'_'+ str(i+1) +'  '+ device.states[i] +'  '+ str(device.valueInChannel) +'  '+ device.collision, file = s)
                   else:
                       print(str(time)+'  '+ device.name +'_'+ str(i+1) +'  '+ device.states[i] +'  '+ str(device.valueInChannel),file = s)
                   
       time+=1

def dfs_disconnect(device):
    device.valueInChannel = -1
    if isinstance(device,myClass.Host):
        device.collision = ' '
    for i in range(len(device.ports)):
        if device.states[i] is not 'null':
            device.states[i] = 'null'
            dfs_disconnect(device.ports[i])




def create(instruction):
    global idCount
    if(instruction[2] == "host"):
        mySet.add(myClass.Host(instruction[3],idCount))
    else:        
        mySet.add(myClass.Hub(instruction[3],int(instruction[4]),idCount))
    idCount+=1
    return


def connect(instruction):
    port_1 = instruction[2].split('_')
    port_2 = instruction[3].split('_')
    device_1 = None
    device_2 = None
    temp = 0
    for j in mySet.Devices:
        if temp == 2:
            break
        for i in j:
            if temp == 2:
                break
            if(i.name == port_1[0]):
                device_1 = i
                temp+=1
            elif(i.name == port_2[0]):
                device_2 = i
                temp+=1         
    device_1.ports[int(port_1[1])-1] = device_2
    device_2.ports[int(port_2[1])-1] = device_1
    mySet.mergeNetworks(device_1,device_2)
    return

def disconnect(instruction):
    port = instruction[2].split('_')
    device1_name = port[0]
    port = int(port[1]) - 1

    device1 = None
    device2 = None 

    #buscando al dispositivo que contiene al puerto que se envio en la instruccion desconectar
    mustBreak = False
    for j in mySet.Devices:
        if mustBreak:
            break
        for i in j:
            if(i.name == device1_name):
                device1 = i
                mustBreak = True
                break

    
    device2 = device1.ports[port]
    dfs_disconnect(device1) if device1.states[port] is 'sending' else dfs_disconnect(device2)

    #buscando al primer dispositivo en los puertos del segundo
    for i in range(len(device2.ports)):
        if device2.ports[i] is not None and device2.ports[i] == device1:
            device2.ports[i]=None
            break
    device1.ports[port] = None     

    mySet.divideNetwork(device1,device2)
    
    return

def send(instruction):
    hostName = instruction[2]
    data = instruction[3]
  
    for i in mySet.Devices:
        for j in i:
            if j.name == hostName:
                j.dataToSend = [x for x in data]
                if not sendDevices.count(j):
                    sendDevices.append(j)
                

    
main()



