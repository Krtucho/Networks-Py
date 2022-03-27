from Host import Host
from Hub import Hub
#from Methods import Methods
signal_time: int = 10

def parser(list):
    


def create_device(type="host", name="", n_ports=1):
    if type == "host":
        return Host(name)
    if type == "hub":
        return Hub(name)
    return None

def start():
    """Metodo principal"""
    items = open("script.txt", 'r')
    lists = items.read().split("\n")
    lists = [item.split() for item in lists]
    
    #instructions=parser(lists)
    time: int = 0
    finished: bool = len(lists) == 0
    index = 0
    
    devices: list = []    
    
    while not finished:
        actual = lists[index]
        while (int)actual[0] == time
            #actual = lists[index]
            



        time++
    
start()