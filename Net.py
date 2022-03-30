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

    def send_bit(host:Host,bit:int):


        return

    def my_device(port:Port):
        name:str=""
        for s in port.name:
            if s == "_":
                break
            name+=s
        if(hosts.__contains__(name)):
            return hosts[name]
        if(hubs.__contains__(name)):
            return hubs[name]
        
    def hub_center(port:Port):#devuelve true si este puerto es el puerto ficticio que queda en el centro del hub y se nombra "name"_0
        pass

    def BFS(s:Host,is_transmitting:bool,logging:bool):
        #pasa por todos los cables y dispositivos alcanzables desde s, si se esta transmitiendo significa que se va a 
        # escribir bit en cada uno de los puertos por los que se pase, en otro caso lo que se va a ir calculando es la 
        #cantidad de bits que se quieren mandar desde distintos host por cada cable(para ver si hay colision)
        queue:list=[]
        d={}
        collision = collision(s)

        #time:int=s.time_to_send_next_bit
        #s.port
        #i:int=0
        hub:bool=false #indica si el ultimo puerto en el que estuve era de un hub(solo se utiliza si se esta transmitiendo)
        queue.append(s.port)
        while len(queue)>0:
            u=queue.pop(0)
            hub= isinstance(my_device(u),Hub)
            for v in self.graph.E[u]:
                if is_transmitting:
                    sending:bool=false#sirve para indicarle a un hub si por el puerto actual se envia, es falso si se esta entrando la informacion por este puerto
                    
                    if !hub and isinstance(my_device(v[0]),Hub):#significa que estoy entrando ahora en el hub
                        sending=false
                    if hub_center(u[0]):sending=true#si mi antecesor es el centro del hub, entonces soy un puerto de salida de este
                        
                    if logging:#si segun el tiempo es momento de escribir en todos los txt
                        v[0].read_bit(s.actual_bit)#se agrega a la lista de los valores annadidos ahora el bit que se esta pasando

                        #v[0].bits_received_in_ms.append(s.actual_bit) #se agrega a la lista de los valores annadidos ahora el bit que se esta pasando
                        my_device(v[0]).write_in_file_logs(v[0],sending,collision)# se manda a escribir al dispositivo su mensaje correspondiente

                    else if len(my_device(v[0]).bits_received_in_ms)==0:#si no esta en momento de escribir pero se sabe que este dispositivo se agrego recientemente porque tiene su lista de bits recibidos vacia
                        v[0].read_bit(s.actual_bit)#se agrega a la lista de los valores annadidos ahora el bit que se esta pasando
                        #v[0].bits_received_in_ms.append(s.actual_bit) 
                        my_device(v[0]).write_in_file_logs(v[0],sending,collision)

                    #if my_device(v[0]).:#si se esta transmitiendo y en este vertice se debe escribir porque se acaba de conectar, se agrega a los bits que recibe el puerto el bit actual
                        #v[0].bits_received_in_ms.append(s.actual_bit) #se agrega a la lista de los valores annadidos ahora el bit que se esta pasando
                        #my_device(v[0]).write_in_file_logs(v[0],sending)
                    #  aqui es donde se indicaria a cada uno escribir lo que tenga que escribir
                if d[v[0]]==None:#d[v] == 0:
                    d[v[0]]=d[u]+1
                v[1]=v[1]+1#para cuando se esten buscando colisiones, aqui se cuentan la cantidad de colisiones que hubo en este cable
                    queue.append(v[0])        
        return d
