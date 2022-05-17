from net import Net
from graph import Graph
from hub import Hub
from switch import Switch
from host import Host
from port import Port



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
            if visited[port]:
                return False
        return True


    @staticmethod
    def modify_net(net:Net,bit:int,time:int,u:Port,v,queue:list,visited:dict,collisions:list,ports_tree:list):
        #sending:bool=False#sirve para indicarle a un hub si por el puerto actual se envia, es falso si se esta entrando la informacion por este puerto
        # if net.hub_center(u):
        #     sending=True#si mi antecesor es el centro del hub, entonces soy un puerto de salida de este
        #change = v[1]!=bit                    
        #se escribe el bit en el cable

        actual_device_u = net.my_device(u)
        actual_device_v = net.my_device(v[0])

        if isinstance(actual_device_u,Hub):
            Hub(actual_device_u).write_bit_in_port(u,bit)
            if(v[1]!=-1):
                collisions.append(v)#si ya esta escrita esa arista es porque hay una colision y el hub lo detecta
                return 
            net.graph.edit_edge_value(u,v[0],bit)

        #net.graph.edit_edge_value(u,v[0],bit)
        

        if isinstance(actual_device_v,Hub):#si es un hub se escribe la informacion que está enviando
            #send_text=""
            if(BFS.discovering_hub(v[0],actual_device_v,visited)):#en caso de que se pase por un puerto de este hub por primera vez
                #send_text="receive"
                Hub(actual_device_v).send_bit(v[0],bit)

            else:#si se esta llegando a un puerto de un hub  por segunda vez
                return

               # send_text="send"
            # send_text=Hub(actual_device).states_ports[v[0]]
            # actual_device.write_msg_in_file(f"{time} {v[0].name} {send_text} {str(bit)}")# se manda a escribir al hub que le llega o recibe el bit correspondiente
        
        if isinstance(actual_device_v,Switch):


            ports_to_send=actual_device_v.send_bit(net,v[0])#pide al switch por los puertos que va a enviar
            queue.append([ p for p in ports_to_send])#agrega a la cola todos los puertos por los que va a enviar el switch


        if isinstance(actual_device_v,Host):
            send_text="receive"
            actual_device_v.write_msg_in_file(f"{time} {v[0].name} {send_text} {str(bit)}")# se manda a escribir al hub que le llega o recibe el bit correspondiente
        
        
        
        
    @staticmethod
    def comprobate_net(net:Net,bit:int,time:int,u,v,queue:list,visited:dict,collisions:list,ports_tree:list):
        actual_device = net.my_device(v[0])

        ports_tree.append([v[0],])


       #if isinstance(actual_device,Host):#si es un host se busca si esta enviando o transmitiendo para detectar la colision
            #aqui importante castear a Host el actual_device
            #if actual_device.writing or actual_device.transmitting:
            #    collisions.append(actual_device)


    @staticmethod
    def bfs(net:Net,f:function,s:Port,bit:int,time:int,queue:list,visited:dict):
        #hub:bool=False #indica si el ultimo puerto en el que estuve era de un hub(solo se utiliza si se esta transmitiendo)
        queue.append(s)
        collisions:list=[]
        ports_tree:list=[]
        #visited:dict = {}
        visited[s] = True

        while len(queue)>0:
            u=queue.pop(0)
            if not net.graph.E.__contains__(u): # en caso de que no tenga aristas
                continue
            for v in net.graph.E[u]:#selecciono la arista                
                if visited.__contains__(v[0]):#si ya esa arista ha sido visitada se salta
                    continue
                f(net,bit,time,u,v,queue,visited,collisions,ports_tree)  #llamo la funcion de cambios en la red
                visited[v[0]]=True
                
            queue.append(v[0])    
        return collisions, ports_tree




#llamada al metodo del bfs
# collisions, ports_treebfs=(net,modify_net,port,bit,time,queue,visited)

# collisions, ports_treebfs=(net,comprobate_net,port,bit,time,queue,visited)




