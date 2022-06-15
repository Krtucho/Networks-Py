from tkinter import N
from graph import Graph
from host import Host
from hub import Hub
from port import Port
from switch import Switch
from frame import Frame
# from bfs import BFS 
import random

class Net:
    def __init__(self, signal_time:int)->None:
        self.signal_time = signal_time
        self.graph = Graph()
        self.hosts = {}
        self.hubs = {}
        self.switchs={}
        
    def create_host(self, name)->None:
        """Crea un host con nombre name"""
        pc = Host(name) # Creando instancia de tipo Host
        self.graph.add_vertex(pc)   # Agregando al grafo el host creado
        self.hosts[pc.name] = pc    # Agregando el host al diccionario que contiene todos los hosts
    
    def create_switch(self,name,n_ports)->None:
        sw=Switch(name,n_ports)
        self.graph.add_vertex(sw)
        self.switchs[sw.name]=sw

    def create_hub(self, name, n_ports):
        """Creando un hub con nombre name y una cantidad n_ports de puertos"""
        hub = Hub(name, n_ports)    # Creando la instancia de tipo Hub
        self.graph.add_vertex(hub)  # Agregando el hub a la lista que contiene a todos los dispositivos
        self.hubs[hub.name] = hub   # Agregando el Hub al dicionario que contiene a todos los hubs
    
    # Mac Address
    def set_mac(self, host: str, mac_address: str):
        target_host:Host = self.my_device_str(host + "_1") # Buscando Host al que le vamos a asignar la Mac
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
        if(self.switchs.__contains__(name)):   # Verificando si el dispositivo esta contenido en el diccionario de switchs
            return self.switchs[name]
        

    def my_device_str(self,port:str):
        """Dado un puerto devuelve el dispositivo en el que se encuentra el mismo"""
        name:str="" # Obteniendo el nombre del dispositivo
        for s in port:
            if s == "_":
                break
            name+=s
        if(self.hosts.__contains__(name)):  # Verificando si el dispositivo esta contenido en el diccionario de hosts
            return self.hosts[name]
        if(self.hubs.__contains__(name)):   # Verificando si el dispositivo esta contenido en el diccionario de hubs
            return self.hubs[name]
        if(self.switchs.__contains__(name)):   # Verificando si el dispositivo esta contenido en el diccionario de switchs
            return self.switchs[name]

   

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
        
        # if self.has_cycles(port1, port2): # Comprobando si no existen ciclos
        #     raise Exception("Conexion innecesaria, esos puertos ya estaban cominicados.")

        self.graph.add_edge(port1, port2, -1)   # Agrega la arista <port1,port2> 
        port1.connect()
        port2.connect()

        hosts_tr_lists = []
        for host in self.hosts.values(): 
            if host.transmitting:
                hosts_tr_lists,p = BFS.bfs(self,BFS.modify_net,host.port,0,time,[],{})
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
                    BFS.bfs(self,BFS.modify_net,host.port, -1, time,[],{})#cuando un host ya transmitio por 10 ms se pone el cable en -1 para que en el siguiente ms cuando se envie algo, todos noten el cambio
                host.update_bit_time(time, False) #Actualizando el bit del host 

        for host in host_transmitting:
                value_to_write = host.actual_bit if not host.time_to_retry > 0 else -1
                BFS.bfs(self,BFS.modify_net,host.port, value_to_write, time,[],{}) # Voy leyendo de todos los dispositivos. 
        # Actualizar todos
        # Deteccion de errores y correctitud
        # Si al terminar de enviar el host q esta en transmitting verificamos con el receptor y en caso de que ocurra colision volvemos a enviar la trama

    def send(self, host:Host, time:int):
        """metodo que se utiliza cuando se envia a un host a enviar un conjunto de bits"""
        host.actual_bit=host.bits_to_send[0]
        self.set_state(host, time, transmitting=True) # Cambiamos el estado y reportamos que el host esta escribiendo 
        host.time_to_send_next_bit = self.signal_time   # Reiniciando el tiempo restante para enviar el siguiente bit
        
        BFS.bfs(self,BFS.modify_net,host.port,host.actual_bit,time,[],{})


    def detect_collisions_on_hubs(host_sending:list):#si se estan enviando varias tramas en el mismo ms
        
        while len(host_sending) > 0:
            target = host_sending[0]
            host_sending.pop(0)

        pass

    def send_many(self, send_list: list, time:int):
        """Procesa todas las instrucciones de send y de send_frame. Si el host comienza a enviar en este ms se verifica si ocurre colision, si ocurre se pone en pendiente, sino, envia.
        Tambien se procesan todos aquellos host que estan en estado de pendiente y se ponen a enviar si no ocurre colision. Por ultimo, si algun host se encontraba transmitiendo, este continuara transmitiendo xq tiene mayor precedencia que los demas."""
        host_sending = []
        # Hosts que comenzaran a estar en writing
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
                # temp_data = "" + instruction[4]
                # data, data_size = Frame.parse_frame_data(instruction[4],method=1)
                data, data_size= Frame.parse_frame_data(instruction[4],method=1)
                host.add_frame(Frame(state="inactive", src_mac=host.mac_address, dst_mac=dst_mac, data_size=data_size,
                                     data=data))    # Annadiendo Frame a lista de frames del host
                #End Added Lines
                # bits = [int(bit) for bit in instruction[3]] # 
                host.bits_to_send += host.frames_list[-1].bits
                host_sending.append(host)

        # Hosts que estaban en pending
        for host in self.hosts.values(): # los hosts que estaban esperando para comenzar a enviar
            if host.pending:
                host.time_to_retry -= 1
                if host.time_to_retry == 0:
                    host.pending = False
                    host.writing = True
                    host_sending.append(host)   # Los sumamos a la lista de hosts que estan enviando en este ms
          
        # Colisiones...Primero hacemos bfs buscando todos aquellos que colisionan con cierto host que se encuentra enviando, de ser asi
        # eliminamos de la lista de los que estan enviando a todos aquellos con los que colisiono este host, si el host se encuentra transmitiendo,
        # le dejamos via libre     
         
          
        #diccionario que va a tener por cada arista que pertenezca a un puerto de un hub, va a devolver el host desde el que se envia
        edges_per_send={}
        collisions=[]
        i=len(host_sending) -1
        # 
        while i > 0:
            target:Host = host_sending[i]
            c,edges=BFS.bfs(self,BFS.comprobate_net,target.port,0,0,[],{})
            # c,edges=self.send(target,time) # Si no ocurrio colision, entonces mandamos a 
            for edge in edges:
                if isinstance(self.my_device(Port(edge[0])),Hub) or isinstance(self.my_device(Port(edge[1])),Hub):
                    if edges_per_send.__contains__(edge):
                        collisions.append(edges_per_send[edge])
                        collisions.append(target)
                    else:
                        edges_per_send[edge]=target
            i-=1

        while len(host_sending) > 0:
            target:Host = host_sending[0]
            if collisions.__contains__(target):                 
                if host.transmitting:   # Si este ya estaba transmitiendo continuara con su transmision porque tiene prioridad
                    continue
                self.set_state(host, time, pending=True, collision=True)                
            else:
                self.send(target,time)
            host_sending.pop(0)
            #aqui se va a comprobar que las colisiones no ocurran en los hubs



            #collisions,port_tree = self.BFS(self,BFS.comprobate_net,target.port, target.bits_to_send[0],time,[],{})
            #cuando este vacia la lista de colisiones hacer send con target 
            # en caso de no estar vacia poner a todos en pendiente(target+pendientes)
            # if len(collisions) > 0:
            #     self.set_state(target, time, pending=True, collision=True)
            #     for host in collisions:  
            #         if not host_sending.__contains__(host): # Si el host no esta contenido en la lista de los host que estan enviando, continua a verificar al siguiente
            #             continue                  
            #         index=host_sending.index(host)  # Indice del host que se envuentra enviando y colisionó.
            #         if host.transmitting:   # Si este ya estaba transmitiendo continuara con su transmision porque tiene prioridad
            #             continue
            #         if index!=-1:  #ver caso de los que estan transmitiendo, en este caso no hacerles nada poner un if para ellos
            #             host_sending.pop(index)
            #             self.set_state(host, time, pending=True, collision=True)
            # else: 
            #     self.send(target,time) # Si no ocurrio colision, entonces mandamos a 


            # host_sending.pop(0)




class BFS:

    @staticmethod 
    def discovering_hub(in_port:Port,h:Hub, visited:dict):
    #Devuelve true si en el bfs actual ya se entro la informacion por algun puerto de ese hub por lo que la funcion del puerto actual
    #es transmitir a partir de ahi
        for port in h.ports:
            if visited[port]:
                return False
        return True

    @staticmethod
    def discovering_switch(in_port:Port,s:Switch,visited:dict):#igual a discovering_hub
        for port in s.ports:
            if visited.__contains__(port):
                return False
        return True


    @staticmethod
    def modify_net(net:Net,bit:int,time:int,u:Port,v,queue:list,visited:dict,collisions:list,edges:list):
        actual_device_u = net.my_device(u)
        actual_device_v = net.my_device(v[0])
        change=not(bit==v[1])
        if not change:#si no hay cambio en la arista no hay nada que hacer
            return
        if isinstance(actual_device_u,Hub):
            Hub(actual_device_u).write_bit_in_port(u,bit)
            if(v[1]!=-1):
                collisions.append(v)#si ya esta escrita esa arista es porque hay una colision y el hub lo detecta
                return 
        
        net.graph.edit_edge_value(u,v[0],bit)
 
        if isinstance(actual_device_v,Hub):#si es un hub se escribe la informacion que está enviando
            if(BFS.discovering_hub(v[0],actual_device_v,visited)):#en caso de que se pase por un puerto de este hub por primera vez
                ports_to_send=Hub(actual_device_v).send_bit(v[0],bit)
                [ queue.append(p) for p in ports_to_send]
            else:#si se esta llegando a un puerto de un hub  por segunda vez
                return


        if isinstance(actual_device_v,Switch):            
            if BFS.discovering_switch(v[0],actual_device_v,visited):  
                ports_to_send = actual_device_v.send_bit(v[0],bit)#pide al switch por los puertos que va a enviar
                [queue.append(p) for p in ports_to_send]#agrega a la cola todos los puertos por los que va a enviar el switch

            else:#si ya se habia llegado a este switch, no se necesita que se vuelva a llegar
                return

        if isinstance(actual_device_v,Host):
            #Port(v[0]).bits_received_in_ms=bit
            if(bit==-1):
                return
            actual_device_v.read_bit(time,bit)
            send_text="receive"            
            actual_device_v.write_msg_in_file(f"{time} {v[0].name} {send_text} {str(bit)}")# se manda a escribir al hub que le llega o recibe el bit correspondiente

        
        
        
    @staticmethod
    def comprobate_net(net:Net,bit:int,time:int,u,v,queue:list,visited:dict,collisions:list,edges:list):
        actual_device = net.my_device(v[0])
        edges.append([u,v[0]])
        



    @staticmethod
    def bfs(net:Net,f,s:Port,bit:int,time:int,queue:list,visited:dict):
        queue.append(s)
        collisions:list=[]
        edges:list=[]
        visited[s] = True

        while len(queue)>0:
            u=queue.pop(0)            
            if not net.graph.E.__contains__(u): # en caso de que no tenga aristas
                continue
            for v in net.graph.E[u]:#selecciono la arista 
                # visited[v[0]]=False
                if visited.__contains__(v[0]):#si ya esa arista ha sido visitada se salta
                    continue
                f(net,bit,time,u,v,queue,visited,collisions,edges)  #llamo la funcion de cambios en la red
                visited[v[0]]=True                
            # queue.append(v[0])    
        return collisions, edges

