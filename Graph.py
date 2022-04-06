from device import Device
from port import Port
from hub import Hub
from host import Host

class Graph:
    def __init__(self):
        self.V = []
        self.E = {}
        
    def add_vertex(self, u: Device)-> None:
        self.V.append(u)
        if isinstance(u, Hub):
            s = u.s # Vertice h_0...El vertice que estara en el centro
            hub_ports: dict = u.ports # Puertos del Hub
            for item in hub_ports.values():
                if item != s:
                    self.add_edge(s, item, -1)
     
    def extract_name(self, port_name:str):
        device_name = port_name.split("_")[0]
        return device_name
        # index = 0
        # for i in range(0, len(port_name)):
        #     if port_name[i] != "_":
                
       
    def search_port(self, port_name: str)-> Port:
        """Dado el nombre de un puerto, devuelve el puerto"""
        target = self.extract_name(port_name)
        for vertex in self.V:
            if vertex.name == target:
                if isinstance(vertex, Hub):
                    # hub_vertex = vertex.ports
                    for port in vertex.ports.values():
                        if port.name == port_name:
                            return port
                else:
                    return vertex.port
        
    def add_edge(self, u: Port, v: Port, w: int): # w es el valor de la arista
        if not self.E.__contains__(u):
            self.E[u] = []
        if not self.E.__contains__(v):
            self.E[v] = []
        
        self.E[u].append([v, w])
        self.E[v].append([u, w])
    
    def edit_edge_value(self, u: Port, v: Port, w: int):
        if not self.E.__contains__(u):
            self.E[u] = []
        if not self.E.__contains__(v):
            self.E[v] = []
            
        for s in self.E[u]:
            if s[0]==v:
                s[1]=w
        for s in self.E[v]:
            if s[0]==u:
                s[1]=w
    
    def my_device(self,port:Port):
        name:str=""
        for s in port.name:
            if s == "_":
                break
            name+=s
            
        for item in self.V:
            if item.name == name:
                return item
        # if(self.V.__contains__(name)):
        #     return self.hosts[name]
        # if(self.hubs.__contains__(name)):
        #     return self.hubs[name]
    
    def hub_center(self, port:Port):#devuelve true si este puerto es el puerto ficticio que queda en el centro del hub y se nombra "name"_0
        if isinstance(self.my_device(port),Hub):
            return port.name[len(port.name)-1]=='0' and port.name[len(port.name)-2]=='_'
        return False
    
    def remove_edge(self, u: Port):
        target = None #[v for v in self.E[u] if v != s]
        if not self.E.__contains__(u):
            return#self.E[u] = []
        temp_list: list = self.E[u]
        
        # if len(temp_list) == 0:
        #     return
        # target = temp_list[0][0]
        u_dev = self.my_device(u)
        
        if isinstance(u_dev, Hub):
            # target = temp_list[0]
            
            # self.E.popitem(u_dev)
            edges = self.E[u]
            vertex_to_remove = None
            edge_to_remove = None
            for edge in edges:
                vertex_to_remove = self.my_device(edge[0])
                if vertex_to_remove !=  None:
                    if isinstance(vertex_to_remove, Hub) and not self.hub_center(edge[0]):
                        # edge[0] == target:
                        # vertex_to_remove = edge[0]
                        self.E[u].remove(edge)
                        edge_to_remove = edge
                        break
                    elif isinstance(vertex_to_remove, Host):
                        self.E[u].remove(edge)
                        edge_to_remove = edge
                        break
                     
            for edge in self.E[edge_to_remove[0]]:
                if edge[0]==u:
                    self.E[edge_to_remove[0]].remove(edge)
                        
        elif isinstance(u_dev, Host):
            if len(temp_list) > 0:
                target = temp_list[0][0]
            # self.E[target].remove()
            
            if target is None:
                return
            
            for edge in self.E[target]:
                if edge[0]==u:
                    self.E[target].remove(edge)
                    break
            
            
            edges = self.E[u]
            edge_to_remove = None
            
            for edge in edges:
                if edge[0] == target:
                    edge_to_remove = edge
                    break
            self.E[u].remove(edge_to_remove)
        
        # for i, v in enumerate(temp_list):
        #     print(v[1])
        #     if v[1] != -1:
        #         target = v[0]
        #         v[0].connected = False
        #         temp_list.pop(i)
                
        #         # temp_list = self.E[v]
        #         self.remove_edge(target)
        #         break
        
  
        
        
        # for v in self.E[u]:            
        #     target = v[0]
        #     v[0].connected = False
        #     for s in self.E[u]:
        #         if s[0]==v:
        #             self.E[u].
        #     for s in self.E[v]:
        #         if s[0]==u:
            
            
            
    def clean_edges_states(self):
        for item in E.values:
            item[1] = -1