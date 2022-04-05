from host import Host
from hub import Hub
from net import Net
# from queue import Queue
import sys

signal_time: int = 10


def create_device(type="host", name="", n_ports=1):
    if type == "host":
        return Host(name)
    if type == "hub":
        return Hub(name)
    return None

def get_inst(lists: list, time: int)->list:
    result = []
    send_list = []
    indexes = []
    for i in range(0, len(lists)):
        # temp_list = lists[i]
        # print(temp_list)
        if int(lists[i][0]) == time and lists[i][1] == "create" :
            result.append(lists[i])
            indexes.append(i)
    for i in range(0, len(lists)):
        if int(lists[i][0]) == time and lists[i][1] == "connect" or lists[i][1] == "disconnect":
            result.append(lists[i])
            indexes.append(i)
            
    for i in range(0, len(lists)):
        if int(lists[i][0]) == time and lists[i][1] == "send":
            send_list.append(lists[i])
            indexes.append(i)
            
    # temp = [item for item in lists if item[0] == time and item[1] ==  "create"]
    return result, send_list
    

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
        instruction, send_list = get_inst(lists, time)
        
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
            # elif instruction.type == "send":
            #     network.send(Net.my_device(instruction.port),instruction.bits, time)#arreglar
        network.send_many(send_list)
        
        network.update(time, signal_time)
        time = time + 1

    for host in network.hosts:
        host.close_output()
        
            




if __name__== '__main__':
    signal_time = 10
    if len(sys.argv) > 1:
        signal_time = int(sys.argv[1])    
    start(signal_time)
