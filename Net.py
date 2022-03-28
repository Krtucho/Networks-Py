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
        # Hago DFS, BFS desde port1 y si llego a port 2 => Existe un ciclo
        pass
    
    def connect(self, port1_name, port2_name):
        if ciclos(port1_name, port2_name):
            raise Exception("No te hagas el gracioso de poner ciclos en el grafo")
        port1 = self.graph.search_port(port1_name)
        port2 = self.graph.search_port(port2_name)
        
        if port1 is None:
            raise Exception()
        if port2 is None:
            raise Exception()
        
        if port1.connected:
            raise...
        if port2.connected:
            raise...
        
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
            
    def BFS(graph:Graph,s:Port):
        queue=[]
        d={}
        i:int
        #i=0
        queue.append(s)
        while queue.count>0:
            u=queue.pop()
            for v in graph.E[u]:
                if d[v] == 0:
                    d[v]=d[u]+1
                    queue.enqueue(v)
        
        return d
