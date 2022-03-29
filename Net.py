from Graph import Graph
from Host import Host
from Hub import Hub

class Net:
    def __init__(self, signal_time:int)->None:
        self.signal_time = signal_time
        self.graph = Graph()
        self.hosts = {}
        self.hubs = {}
        
    def create_host(self, name):
        pc = Host(name)
        self.graph.add_vertex(pc)
        self.hosts[pc.name] = pc
    
    def create_hub(self, name, n_ports):
        hub = Hub(name, n_ports)
        self.graph.add_vertex(hub)
        # self.hubs.
    
    def ciclos(self, port1, port2):
        d=BFS(port1,graph,false)
        return d[port2]!=None
        # Hago DFS, BFS desde port1 y si llego a port 2 => Existe un ciclo
        #pass
    
    def connect(self, port1_name, port2_name):
        
        port1 = self.graph.search_port(port1_name)
        port2 = self.graph.search_port(port2_name)
        
        if port1 is None:
            raise Exception("Puerto_1 vacio")
        if port2 is None:
            raise Exception("Puerto_2 vacio")
        
        if port1.connected:
            raise Exception("Puerto_1 conectado a alguien mas")
        if port2.connected:
            raise Exception("Puerto_2 conectado a alguien mas")
        
        if ciclos(port1, port2):
            raise Exception("Conexion innecesaria, esos puertos ya estaban cominicados.")

        self.graph.add_edge(port1, port2)
        port1.connect()
        port2.connect()
    
    def disconnect(self, port):
        port1 = self.graph.search_port(port)
        self.graph.remove_edge(port1)
    
    def update():
        for host in hosts:
            if host.transmitting:
                do_something()
        for host in hosts:
            read_info_and_chek()
            
    def BFS(graph:Graph,s:Port,transmitting:bool):
        queue:list=[]
        d={}
        #i:int=0
        queue.append(s)
        while len(queue)>0:
            u=queue.pop(0)
            for v in graph.E[u]:
                if d[v]==None:#d[v] == 0:
                    d[v]=d[u]+1
                    #aqui es donde viene la parte de verificar si se esta transmitiendo para escribir y en caso de que si, escribir en el txt
                    #aqui poner lo de que el host lea el valor 
                    queue.append(v)        
        return d
