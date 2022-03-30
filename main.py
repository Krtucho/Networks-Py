import sys
from Host import Host
from Hub import Hub
from Net import Net
from queue import Queue

signal_time: int = 10


def create_device(type="host", name="", n_ports=1):
    if type == "host":
        return Host(name)
    if type == "hub":
        return Hub(name)
    return None

def get_inst(lists: list, time: int)->list:
    result = []
    for i in range(0, len(lists)):
        if lists[i][0] == time and lists[i][1] == "create" :
            result.append(lists.pop(i))
    for i in range(0, len(lists)):
        if lists[i][0] == time and lists[i][1] == "connect" or lists[i][1] == "disconnect":
            result.append(lists.pop(i))
            
    for i in range(0, len(lists)):
        if lists[i][0] == time and lists[i][1] == "send":
            result.append(lists.pop(i))
            
    # temp = [item for item in lists if item[0] == time and item[1] ==  "create"]
    return result
    

def start(signal_time):
    """Metodo principal"""
    items = open("script.txt", 'r')
    lists = items.read().split("\n")
    lists = [item.split() for item in lists]
    print(lists)
    
    time: int = 0
    finished: bool = len(lists) == 0
    index = 0
    
    devices: list = []
    
    network = Net(signal_time)
    
    while not finished:
        # actual = lists[index]
        # while actual[0] == 
        #     actual = lists[index]
        instruction = get_inst(lists, time)
        
        while len(instruction) > 0:
            
            if instruction.type == "create":
                if "host":
                    network.create_host(list[3])
                elif "hub":
                    network.create_hub(list[3],list[4])
            elif instruction.type == "connect":
                network.connect(instruction.port1, instruction.port2)
            elif instruction.type == "disconnect":
                network.disconnect(instruction.port)
            elif instruction.type == "send":
                network.send(instruction.port)
        network.update(time, signal_time)
        time = time + 1
        
            




if __name__== '__main__':
    signal_time = 10
    if len(sys.argv) > 1:
        signal_time = int(sys.argv[1])    
    start(signal_time)
