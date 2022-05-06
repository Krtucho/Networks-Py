from graph import Graph
from host import Host
from hub import Hub
from port import Port
from switch import Switch

from frame import Frame

import random

class Net:
    def __init__(self, signal_time:int)->None:
        self.signal_time = signal_time
        self.graph = Graph()
        self.hosts = {}
        self.hubs = {}
        
    def create_host(self, name)->None:
        """Crea un host con nombre name"""
        pc = Host(name) # Creando instancia de tipo Host
        self.graph.add_vertex(pc)   # Agregando al grafo el host creado
        self.hosts[pc.name] = pc    # Agregando el host al diccionario que contiene todos los hosts
    
    def create_hub(self, name, n_ports):
        """Creando un hub con nombre name y una cantidad n_ports de puertos"""
        hub = Hub(name, n_ports)    # Creando la instancia de tipo Hub
        self.graph.add_vertex(hub)  # Agregando el hub a la lista que contiene a todos los dispositivos
        self.hubs[hub.name] = hub   # Agregando el Hub al dicionario que contiene a todos los hubs
    
    # Mac Address
    def set_mac(self, host: str, mac_address: str):
        target_host:Host = self.my_device(host + "_1") # Buscando Host al que le vamos a asignar la Mac
        target_host.mac_address = mac_address # Asignando mac
    
#region Utiles
    
    def my_device(self,port:Port):
        """Dado un puerto devuelve el dispositivo en el que se encuentra el mismo"""
        name:str="" # Obteniendo el nombre del dispositivo
        for s in port.name:
            if s == "_":
                break
            name+=s
        if(self.hosts.__contains__(name)):  # Verificando si el dispositivo esta contenido en el diccionario de hosts
            return self.hosts[name]
        if(self.hubs.__contains__(name)):   # Verificando si el dispositivo esta contenido en el diccionario de hubs
            return self.hubs[name]

    def hub_center(self, port:Port):
        """Devuelve true si este puerto es el puerto ficticio que queda en el centro del hub y se nombra "name"_0"""
        if isinstance(self.my_device(port),Hub):
            return port.name[len(port.name)-1]=='0' and port.name[len(port.name)-2]=='_'
        return False

    def BFS(self, s:Port,bit:int,time:int,checking:bool):
        queue:list=[]
        hub:bool=False #indica si el ultimo puerto en el que estuve era de un hub(solo se utiliza si se esta transmitiendo)
        queue.append(s)
        collisions:list=[]
        ports_tree:list=[]
        visited:dict = {}
        visited[s] = True
        while len(queue)>0:
            u=queue.pop(0)
            if not self.graph.E.__contains__(u): # Quitar x si acaso
                continue
            for v in self.graph.E[u]:
                if visited.__contains__(v[0]):
                    continue
                if not checking:#es un bfs para enviar informacion por los cables

                    sending:bool=False#sirve para indicarle a un hub si por el puerto actual se envia, es falso si se esta entrando la informacion por este puerto
                    if self.hub_center(u):
                        sending=True#si mi antecesor es el centro del hub, entonces soy un puerto de salida de este
                    change = v[1]!=bit                    
                    #se escribe el bit en el cable
                    self.graph.edit_edge_value(u,v[0],bit)
                    actual_device = self.my_device(v[0])
                    if isinstance(actual_device,Hub):#si es un hub se escribe la informacion que está enviando 
                        send_text = "send" if sending else "receive"
                        if not self.hub_center(v[0]) and bit!=-1 and change:
                            actual_device.write_msg_in_file(f"{time} {v[0].name} {send_text} {str(bit)}")# se manda a escribir al hub que le llega o recibe el bit correspondiente
                    if isinstance(actual_device,Host) and bit !=-1 and change:
                        send_text="receive"
                        actual_device.write_msg_in_file(f"{time} {v[0].name} {send_text} {str(bit)}")# se manda a escribir al hub que le llega o recibe el bit correspondiente
                else:#o sea es un bfs para detectar colisiones
                    actual_device = self.my_device(v[0])
                    ports_tree.append(v[0])
                    if isinstance(actual_device,Host):#si es un host se busca si esta enviando o transmitiendo para detectar la colision
                        #aqui importante castear a Host el actual_device
                        if actual_device.writing or actual_device.transmitting:
                            collisions.append(actual_device)
                visited[v[0]]=True
                
                queue.append(v[0])    
        return collisions, ports_tree



    def has_cycles(self, port1, port2):
        """Verifica si existen ciclos en la red(el grafo)"""
        collisions,ports_tree=self.BFS(port1,0,0,True)
        return ports_tree.__contains__(port2)

#endregion

    def set_state(self, host:Host, time, transmitting=False, writing=False, pending=False, collision=False):
        """Para cambiar el estado de un host a escribiendo, transmitiendo o pendiente"""
        host.transmitting = transmitting
        host.writing = writing
        host.pending = pending
        if collision:
            host.time_to_retry = random.randint(1, 3)
            host.actual_bit=host.bits_to_send[0]
        host.write_in_file_logs(time, sending=True, collision=collision) # Escribiendo en el archivo del dispositivo, se utiliza cuando el dispositivo este enviando

    def connect(self, port1_name, port2_name, time):
        """Conecta el puerto con nombre port1_name al puerto con nombre port2_name"""
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
        
        if self.has_cycles(port1, port2): # Comprobando si no existen ciclos
            raise Exception("Conexion innecesaria, esos puertos ya estaban cominicados.")

        self.graph.add_edge(port1, port2, -1)   # Agrega la arista <port1,port2> 
        port1.connect()
        port2.connect()

        hosts_tr_lists = []
        for host in self.hosts.values(): 
            if host.transmitting:
                hosts_tr_lists,p = self.BFS(host.port,0,time,True)
                if len(hosts_tr_lists)>0:
                    self.set_state(time, host, pending=True)
                    for coll_host in hosts_tr_lists:
                        self.set_state(time, coll_host, pending=True)
                    break

    def disconnect(self, port):
        port1 = self.graph.search_port(port)
        self.graph.remove_edge(port1)
    
    def is_finished(self):
        for host in self.hosts.values():
             if host.pending or host.transmitting or host.writing:
                 return False
        return True
    
    def update(self, time, signal_time):
        host_transmitting = []
        
        for host in self.hosts.values():
            if host.transmitting:
                host_transmitting.append(host)
                # Voy modificando todos los cables. Escribir valor en cable, null si hay cambio
                if host.time_to_send_next_bit == 0:
                    self.BFS(host.port, -1, time, False)
                host.update_bit_time(time, False) #Actualizando el bit del host 

        for host in host_transmitting:
                value_to_write = host.actual_bit if not host.time_to_retry > 0 else -1
                self.BFS(host.port, value_to_write, time, False) # Voy leyendo de todos los dispositivos. 
        #Actualizar todos
        # Deteccion de errores y correctitud
        # Si al terminar de enviar el host q esta en transmitting verificamos con el receptor y en caso de que ocurra colision volvemos a enviar la trama

    def send(self, host:Host, time:int):
        """metodo que se utiliza cuando se envia a un host a enviar un conjunto de bits"""
        host.actual_bit=host.bits_to_send[0]
        self.set_state(host, time, transmitting=True) # Cambiamos el estado y reportamos que el host esta escribiendo 
        host.time_to_send_next_bit = self.signal_time   # Reiniciando el tiempo restante para enviar el siguiente bit
        
        self.BFS(host.port,host.actual_bit,time,False)


    def send_many(self, send_list: list, time:int):
        """Procesa todas las instrucciones de send y de send_frame"""
        host_sending = []
        for instruction in send_list: # Iterando por las instrucciones de enviar en la lista que contiene al inicio las instrucciones de send y luego las de send_frame
            if instruction[1] == "send":
                host = self.my_device(self.graph.search_port(instruction[2]))
                host.writing = True
                bits = [int(bit) for bit in instruction[3]]
                host.bits_to_send += bits
                host_sending.append(host)
            elif instruction[1] == "send_frame": # Creamos el Frame en el host a enviar, annadimos cada bit de la trama a enviar a los bits que tiene q enviar el host, annadimos este host a la lista de host que se encuentran enviando
                host:Host = self.my_device(self.graph.search_port(instruction[2])) # Busco el host que commenzara a enviar
                host.writing = True # Este Host esta escribiendo
                # Added Lines
                dst_mac = instruction[3]    # Mac de destino
                data, data_size = Frame.parse_frame_data(instruction[4],method=1)
                host.add_frame(Frame(state="inactive", src_mac=host.mac_address, dst_mac=dst_mac, data_size=data_size,
                                     data=data))    # Annadiendo Frame a lista de frames del host
                #End Added Lines
                bits = [int(bit) for bit in instruction[3]] # 
                host.bits_to_send += bits
                host_sending.append(host)
        
        for host in self.hosts.values():
            if host.pending:
                host.time_to_retry -= 1
                if host.time_to_retry == 0:
                    host.pending = False
                    host.writing = True
                    host_sending.append(host)
        while len(host_sending) > 0:
            target = host_sending[0]
            collisions,port_tree = self.BFS(target.port, target.bits_to_send[0],time,True)
            #cuando este vacia la lista de colisiones hacer send con target 
            # en caso de no estar vacia poner a todos en pendiente(target+pendientes)
            if len(collisions) > 0:
                self.set_state(target, time, pending=True, collision=True)
                for host in collisions:  
                    if not host_sending.__contains__(host):
                        continue                  
                    index=host_sending.index(host)
                    if host.transmitting:
                        continue
                    if index!=-1:  #ver caso de los que estan transmitiendo, en este caso no hacerles nada poner un if para ellos
                        host_sending.pop(index)
                        self.set_state(host, time, pending=True, collision=True)
            else: 
                self.send(target,time)
            host_sending.pop(0)