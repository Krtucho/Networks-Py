from graph import Graph
from host import Host
from hub import Hub
from port import Port
import random

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
        self.hubs[hub.name] = hub
        # self.hubs.
    
#region Utiles
    
    def my_device(self,port:Port):
        name:str=""
        for s in port.name:
            if s == "_":
                break
            name+=s
        if(self.hosts.__contains__(name)):
            return self.hosts[name]
        if(self.hubs.__contains__(name)):
            return self.hubs[name]

    def hub_center(self, port:Port):#devuelve true si este puerto es el puerto ficticio que queda en el centro del hub y se nombra "name"_0
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
            hub= isinstance(self.my_device(u),Hub)
            for v in self.graph.E[u]:
                if visited.__contains__(v[0]):
                    continue
                if not checking:#es un bfs para enviar informacion por los cables

                    sending:bool=False#sirve para indicarle a un hub si por el puerto actual se envia, es falso si se esta entrando la informacion por este puerto
                    if self.hub_center(u):
                        sending=True#si mi antecesor es el centro del hub, entonces soy un puerto de salida de este
                    
                    v[1]=bit #se escribe el bit en el cable
                    
                    actual_device = self.my_device(v[0])
                    if isinstance(actual_device,Hub):#si es un hub se escribe la informacion que está enviando 
                        send_text = "send" if sending else "receive"
                        actual_device.write_msg_in_file(f"{time} {v[0].name} {send_text} {str(bit)}")# se manda a escribir al hub que le llega o recibe el bit correspondiente
                        
                        # if len(self.my_device(v[0]).bits_received_in_ms)==0:#si no esta en momento de escribir pero se sabe que este dispositivo se agrego recientemente porque tiene su lista de bits recibidos vacia
                        #     v[0].read_bit(s.actual_bit)#se agrega a la lista de los valores annadidos ahora el bit que se esta pasando
                        #     actual_device.write_in_file_logs(f"{time} {v[0].name} receive {bit}")# se manda a escribir al hub que le llega o recibe el bit correspondiente
                        
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
        #return False
        # host1= self.my_device(port1)
        # host2= self.my_device(port2)
        # host2_transmitting=host2.transmitting
        # host2.transmitting=True
        collisions,ports_tree=self.BFS(port1,0,0,True)
        # host2.transmitting=host2_transmitting
        return ports_tree.__contains__(port2)

    # def has_cycles(self, port1, port2):
    #     return False
        # d=BFS(port1,0)
        # return d[port2]!=None
        # Hago DFS, BFS desde port1 y si llego a port 2 => Existe un ciclo
                           

#endregion

    def set_pending_state(self, host:Host, time):
        host.transmitting = False
        host.sending = False
        host.pending = True
        host.time_to_retry = random.randint(1, 3)
        self.write_in_file_logs(time, host.port ,sending=True, collision = True)

    def connect(self, port1_name, port2_name, time):
        
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
        
        if self.has_cycles(port1, port2):
            raise Exception("Conexion innecesaria, esos puertos ya estaban cominicados.")

        self.graph.add_edge(port1, port2, -1)
        port1.connect()
        port2.connect()

        hosts_tr_lists = []
        for host in self.hosts.values():
            if host.transmitting:
                hosts_tr_lists,p = self.BFS(host.port,0,time,True)
                if len(hosts_tr_lists)>0:
                    self.set_pending_state(time, host)
                    for coll_host in hosts_tr_lists:
                        self.set_pending_state(time, coll_host)
                    break

        
        # if len(hosts_tr_lists) != 0:
            
        


    
    def disconnect(self, port):
        port1 = self.graph.search_port(port)
        self.graph.remove_edge(port1)
    
    def is_finished(self):
        for host in self.hosts.values():
             if host.pending or host.transmitting or host.writing:
                 return False
        return True
  
    
    def update(self, time, signal_time):
        for host in self.hosts.values():
            if host.transmitting:
                value_to_write = host.actual_bit if not host.time_to_retry > 0 else -1
                self.BFS(host.port, host.actual_bit, time, False) # Voy modificando todos los cables. Escribir valor en cable, null si hay cambio
                host.update_bit_time(time, False) #Actualizando el bit del host 


        # for host in self.hosts:
        #     if host.transmitting:
                
        #Todos leen y si el valor es nulo no escriben, si hubo un cambio entre el valor q tenian antes escriben enn el txt
        for host in self.hosts.values():
            if host.change_detected(host.actual_bit):
                host.write_in_file_logs(time, host.port, False, False)

        #Actualizar todos

        #Hasta aca llega el update()

        #  for host in hosts:
        #     if host.transmitting #or (host.pending and host.time_to_send_next_bit == 0):
        #         # if not collision(host):
        #         # logging: bool = False
        #         if host.time_to_send_next_bit == signal_time:
        #             logging = True
        #         #bfs(host, True, logging)
        #         BFS(host,)

        # for host in self.hosts:
        #     if host.writing:
        #         if self.graph.E[host][1]==host.actual_bit  #no hay colision #collision(host):
        #             # bfs(host)
        #             host.transmitting = True
        #             host.sending = False

        #         elif collision(host):
        #             host.sending = False
        #             host.pending = True
        #             host.time_to_retry = randint(1, 3)
        #             self.write_in_file_logs(self, ms=signal_time, host.port ,sending=True, collision = True)
        
        # for host in hosts:
        #     read_info_and_chek()
        
        



        # self.graph.clean_edges_states()


    # def send(host:Host,data:list, time:int):#metodo que se utiliza cuando se envia a un host a enviar un conjunto de bits
    #     host.send(data,time)
    #     send_bit(host,time)
    #     return 


    # def send_bit(host:Host,time:int):#metodo que se utiliza a la hora de enviar cada bit
    #     host.actual_bit=host.bits_to_send[0]
    #     BFS(host,host.actual_bit,time)
    #     return

    def send(self, host:Host, time:int):#metodo que se utiliza cuando se envia a un host a enviar un conjunto de bits
        #host.send(data,time)
        host.actual_bit=host.bits_to_send[0]
        #send_bit(host,time)
        self.BFS(host.port,host.actual_bit,time,False)


    def send_many(self, send_list: list, time:int):
        host_sending = []
        for instruction in send_list:
            host = self.my_device(self.graph.search_port(instruction[2]))
            host.writing = True
            bits = [int(bit) for bit in instruction[3]]
            host.bits_to_send += bits
            host_sending.append(host)
        
        for host in self.hosts.values():
            if host.pending:
                host.pending = False
                host.writing = True
                host_sending.append(host)
        while len(host_sending) > 0:
            target = host_sending[0]# if len(host_sending) > 0 else None
            #if target != None:
            collisions,port_tree = self.BFS(target.port, target.bits_to_send[0],time,True)
            #cuando este vacia la lista de colisiones hacer send con target 
            # en caso de no estar vacia poner a todos en pendiente(target+pendientes)
            if len(collisions) > 0:
                self.set_pending_state(target, time)
                for host in collisions:                    
                    index=host_sending.index(host)
                    if host.transmitting:
                        continue
                    if index!=-1:  #ver caso de los que estan transmitiendo, en este caso no hacerles nada poner un if para ellos
                        host_sending.pop(index)
                        self.set_pending_state(host, time)
                        # host.pending = True
                        # host.writing =  False
                        # host.transmitting = False
            else: 
                self.send(target,time)
            host_sending.pop(0)




