from host import Host
from hub import Hub
from switch import Switch
from router import Router
from net import *
import sys

signal_time: int = 10


def create_device(type="host", name="", n_ports=1):
    if type == "host":
        return Host(name)
    if type == "hub":
        return Hub(name)
    if type == "switch":
        return Switch(name)
    if type == "router":
        return Router(name)
    return None

# def get_inst(lists: list, time: int)->list:
#     result = []
#     send_list = []
     
#     for item in lists:
#         if int(item[0]) == time and item[1] == "create" :
#             result.append(item)

#     for item in lists:
#         if int(item[0]) == time and item[1] == "mac" :
#             result.append(item)    

#     for item in lists:
#         if (int(item[0]) == time) and (item[1] == "connect" or item[1] == "disconnect"):
#             result.append(item)
            
#     for item in lists:
#         if int(item[0]) == time and item[1] == "send":
#             send_list.append(item)
            
#     for item in lists:
#         if int(item[0]) == time and item[1] == "send_frame":
#             send_list.append(item)
    
#     for item in result:
#         if lists.__contains__(item):
#             lists.remove(item)
            
#     for item in send_list:
#         if lists.__contains__(item):
#             lists.remove(item)
            
#     return result, send_list
    
def get_inst(lists: list, time: int)->list:
    result = []
    send_list = []
     
    for item in lists:
        if int(item[0]) == time and item[1] == "create" :
            result.append(item)
    for item in lists:
        if int(item[0]) == time and item[1] == "mac" :
            result.append(item)
            
    for item in lists:
        if (int(item[0]) == time) and (item[1] == "connect" or item[1] == "disconnect"):
            result.append(item)
            
    for item in lists:
        if int(item[0]) == time and item[1] == "route" :
            result.append(item)
            
    for item in lists:
        if int(item[0]) == time and item[1] == "send":
            send_list.append(item)
            
    for item in lists:
        if int(item[0]) == time and item[1] == "send_frame":
            send_list.append(item)
    
    for item in lists:
        if int(item[0]) == time and item[1] == "send_packet":
            send_list.append(item)
    
    for item in result:
        if lists.__contains__(item):
            lists.remove(item)
            
    for item in send_list:
        if lists.__contains__(item):
            lists.remove(item)
            
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
        instruction, send_list = get_inst(lists, time)
        print(time)
        while len(instruction) > 0:
            actual_inst = instruction[0]
            if actual_inst[1] == "create":
                if  actual_inst[2] == "host":
                    network.create_host(actual_inst[3])
                elif  actual_inst[2] == "hub":
                    network.create_hub(actual_inst[3],actual_inst[4])
                elif  actual_inst[2] == "switch":
                    network.create_switch(actual_inst[3],actual_inst[4])
                elif actual_inst[2] == "router":
                    network.create_router(actual_inst[3], actual_inst[4])
            elif actual_inst[1] == "mac":
                network.set_mac(actual_inst[2], actual_inst[3])
            elif actual_inst[1] == "connect":
                network.connect(actual_inst[2], actual_inst[3], time)
            elif actual_inst[1] == "disconnect":
                network.disconnect(actual_inst[2])
            elif actual_inst[1] == "route":
                if actual_inst[2] == "reset":
                    network.reset_route(actual_inst[3])
                elif actual_inst[2] == "add":
                    network.add_route()
                elif actual_inst[2] == "delete":
                    
            instruction.pop(0)
            
            
        network.send_many(send_list, time)
        # Asumo que el send_frame va por aca
        
        network.update(time, signal_time)
        time = time + 1
        
        finished = not len(lists) and is_finished(network)

    items.close()

    def reset_route(self, router_name):
        router:Router = self.routers[router_name]
        if router == None:
            return None
        router.routes_table = {}
        
    def add_route(self, name, destination, mask, getaway, interface)
        router:Router = self.routers[name]
        if router == None:
            return None
        if router.routes_table.__contains__(mask):
            
        router.routes_table = {}

if __name__== '__main__':
    signal_time = 10
    if len(sys.argv) > 1:
        signal_time = int(sys.argv[1])    
    start(signal_time)