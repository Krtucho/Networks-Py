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
    # indexes = []
    # for i in range(0, len(lists)):
    #     # temp_list = lists[i]
    #     # print(temp_list)
    #     if int(lists[i][0]) == time and lists[i][1] == "create" :
    #         result.append(lists[i])
    #         indexes.append(i)
    # for i in range(0, len(lists)):
    #     if int(lists[i][0]) == time and lists[i][1] == "connect" or lists[i][1] == "disconnect":
    #         result.append(lists[i])
    #         indexes.append(i)
            
    # for i in range(0, len(lists)):
    #     if int(lists[i][0]) == time and lists[i][1] == "send":
    #         send_list.append(lists[i])
    #         indexes.append(i)
     
    for item in lists:
        if int(item[0]) == time and item[1] == "create" :
            result.append(item)

            
    for item in lists:
        if int(item[0]) == time and item[1] == "connect" or item[1] == "disconnect":
            result.append(item)
            
    for item in lists:
        if int(item[0]) == time and item[1] == "send":
            send_list.append(item)
            
    for item in result:
        if lists.__contains__(item):
            lists.remove(item)
            
    for item in send_list:
        if lists.__contains__(item):
            lists.remove(item)
            
    #         indexes.append(i)
            
    #         indexes.append(i)
    #         # temp_list = lists[i]
    #     # print(temp_list)
    #     if int(lists[i][0]) == time and lists[i][1] == "create" :
    #         result.append(lists[i])
    #         indexes.append(i)
     
    # result.remove()
    # result = [item for item in result if not int(item[0]) == time]
    # for i in indexes:
    #     lists.pop(i)       
    # temp = [item for item in lists if item[0] == time and item[1] ==  "create"]
    return result, send_list
    
    
def is_finished(network:Net):
    return network.is_finished()

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
        print(len(instruction))
        while len(instruction) > 0:
            actual_inst = instruction[0]
            if actual_inst[1] == "create":
                if  actual_inst[2] == "host":
                    network.create_host(actual_inst[3])
                elif  actual_inst[2] == "hub":
                    network.create_hub(actual_inst[3],actual_inst[4])
            elif actual_inst[1] == "connect":
                network.connect(actual_inst[2], actual_inst[3], time)
            elif actual_inst[1] == "disconnect":
                network.disconnect(actual_inst[2])
            # elif instruction.type == "send":
            #     network.send(Net.my_device(instruction.port),instruction.bits, time)#arreglar
            instruction.pop(0)
        network.send_many(send_list, time)
        
        network.update(time, signal_time)
        time = time + 1
        
        finished = not len(lists) and is_finished(network)

    for host in network.hosts.values():
        host.close_output()
        
            
    items.close()



if __name__== '__main__':
    signal_time = 10
    if len(sys.argv) > 1:
        signal_time = int(sys.argv[1])    
    start(signal_time)
