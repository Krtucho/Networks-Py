from device import Device
from port import Port
from hub import Hub

class Graph:
    def __init__(self):
        self.V = []
        self.E = {}
        
    def add_vertex(self, u: Device)-> None:
        self.V.append(u)
        if isinstance(u, Hub):
            s = u.s # Vertice h_0...El vertice que estara en el centro
            hub_ports: dict = u.ports # Puertos del Hub
            for item in hub_ports:
                if item != s:
                    self.add_edge(s, item, -1)
        
    def search_port(self, port)-> Port:
        return Port("aaa")
        
        
    def add_edge(self, u: Port, v: Port, w: int): # w es el valor de la arista
        if self.E[u] == None:
            self.E[u] = []
        if self.E[v] == None:
            self.E[v] = []
        
        self.E[u].append((v, w))
        self.E[v].append((u, w))
        
    def remove_edge(self, u: Port):
        target = None #[v for v in self.E[u] if v != s]
        temp_list: list = self.E[u]
        
        
        for v, i in enumerate(temp_list):
            if v[1] != -2:
                target = v[0]
                v[0].connected = False
                temp_list.pop(i)
                
                # temp_list = self.E[v]
                self.remove_edge(target)
                break
            
        def clean_edges_states(self):
            for item in E.values:
                item[1] = -1