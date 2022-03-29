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

    def send(host:Host,data:list):
        
        return 

    def sen_bit(host:Host,bit:int):


        return

    def my_device(port:Port):
        


    def BFS(s:Host,transmitting:bool):
        #pasa por todos los cables y dispositivos alcanzables desde s, si se esta transmitiendo significa que se va a 
        # escribir bit en cada uno de los puertos por los que se pase, en otro caso lo que se va a ir calculando es la 
        #cantidad de bits que se quieren mandar desde distintos host por cada cable(para ver si hay colision)
        queue:list=[]
        d={}
        #s.port
        #i:int=0
        hub:bool=false #indica si el ultimo puerto en el que estuve era de un hub(solo se utiliza si se esta transmitiendo)
        queue.append(s.port)
        while len(queue)>0:
            u=queue.pop(0)
            hub=u.
            for v in self.graph.E[u]:
                if transmitting:
                    
                    v[0].bits_received_in_ms.append(s.actual_bit) #si se esta transmitiendo, se agrega a los bits que recibe el puerto el bit actual
                    #  aqui es donde se indicaria a cada uno escribir lo que tenga que escribir
                if d[v[0]]==None:#d[v] == 0:
                    d[v[0]]=d[u]+1
                v[1]=v[1]+1
                    queue.append(v[0])        
        return d
