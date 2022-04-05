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
    
#region Utiles
    
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
        return port.name[len(port.name)-1]=='0' and port.name[len(port.name)-2]=='_'

    #  def write_in_file_logs(self, ms: int,port: Port,sending: bool, collision: bool):
    #         bit = port.bits_received_in_ms[-1]
    #     state = "send" if sending else "receive"
    #     name = port.name
    #     ok = "collision" if collision else "ok"
    #     if sending:
    #         self.write_msg_in_file(f"{ms} {name} {state} {bit} {ok}")
    #     elif not sending:
    #         self.write_msg_in_file(f"{ms} {name} {state} {bit}")




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
                    
                    if not hub and isinstance(my_device(v[0]),Hub):#significa que estoy entrando ahora en el hub
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




    # def BFS(s:Host,bit:int,time:int):#transmite las informaciones que se envian a todos los dispositivos alcanzables
    #     queue:list=[]
    #     queue.append(s.port)
    #     while len(queue)>0:
    #         u=queue.pop(0)
    #         for v in self.graph.E[u]:
    #             sending:bool=hub_center(u[0])#sirve para indicarle a un hub si por el puerto actual se envia, es falso si se esta entrando la informacion por este puerto
    #                                          #si mi antecesor es el centro del hub, entonces soy un puerto de salida de este
    #                 if v[1] != None:
    #                     value=v[1]^bit# si hay valor en el cable se hace xor entre este y el bit que se esta enviando y esto es lo que se almacena en el cable
    #                 else: value=bit# si en el cable no hay valor, se pone el bit que se esta enviando
    #                 change_bit=v[1]==value
    #                 v[1]=value 
    #                 actual_device = my_device(v[0])
    #                 if isinstance(actual_device,Hub) and change:#si es un hub y ademas se cambio la informaci'on que se esta enviando
    #                     actual_device.write_in_file_logs(f"{time} {v[0].name} {"send" if sending else "receive":} {value}")# se manda a escribir al hub que le llega o recibe el bit correspondiente
                    


    def ciclos(self, port1, port2):
        d=BFS(port1,0)
        return d[port2]!=None
        # Hago DFS, BFS desde port1 y si llego a port 2 => Existe un ciclo
                           

#endregion


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

        hosts_tr_lists = []
        for host in self.host:
            if host.transmitting:
                hosts_tr_lists = BFS()
                break

        if len(hosts_tr_lists) != 0:
            for host in hosts_tr_lists:
                host.transmitting = False
                host.sending = False
                host.pending = True
                host.time_to_retry = randint(1, 3)
                self.write_in_file_logs(self, ms=signal_time, host.port ,sending=True, collision = True)
        


    
    def disconnect(self, port):
        port1 = self.graph.search_port(port)
        self.graph.remove_edge(port1)
    
     
  
    
    def update(self, time, signal_time):
        for host in hosts:
            if host.transmitting:
                value_to_write = host.actual_bit if not host.time_to_retry > 0 else -1
                BFS(host) # Voy modificando todos los cables. Escribir valor en cable, null si hay cambio
                host.update_bit_time(time, False) #Actualizando el bit del host 


        for host in self.hosts:
            if host.transmitting:
                
        #Todos leen y si el valor es nulo no escriben, si hubo un cambio entre el valor q tenian antes escriben enn el txt
        for host in self.hosts:
            if host.change_detected(host.actual_bit):
                write_in_file_log(host)

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


    def send(host:Host,data:list, time:int):#metodo que se utiliza cuando se envia a un host a enviar un conjunto de bits
        host.send(data,time)
        send_bit(host,time)
        return 

    def send_bit(host:Host,time:int):#metodo que se utiliza a la hora de enviar cada bit
        host.actual_bit=host.bits_to_send[0]
        BFS(host,host.actual_bit,time)
        return


