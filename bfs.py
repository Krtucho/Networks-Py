from net import Net
from graph import Graph
from hub import Hub
from switch import Switch
from host import Host
from port import Port



class BFS:

    @staticmethod
    def modify_net(net:Net,bit:int,time:int,u,v,queue:list,visited:dict,collisions:list,ports_tree:list):
        #sending:bool=False#sirve para indicarle a un hub si por el puerto actual se envia, es falso si se esta entrando la informacion por este puerto
        # if net.hub_center(u):
        #     sending=True#si mi antecesor es el centro del hub, entonces soy un puerto de salida de este
        change = v[1]!=bit                    
        #se escribe el bit en el cable
        net.graph.edit_edge_value(u,v[0],bit)
        actual_device = net.my_device(v[0])

        if(bit!=-1 and change):
            if isinstance(actual_device,Hub):#si es un hub se escribe la informacion que está enviando 
                send_text = "send" if sending else "receive"
                if not net.hub_center(v[0]):
                    actual_device.write_msg_in_file(f"{time} {v[0].name} {send_text} {str(bit)}")# se manda a escribir al hub que le llega o recibe el bit correspondiente
            if isinstance(actual_device,Host):
                send_text="receive"
                actual_device.write_msg_in_file(f"{time} {v[0].name} {send_text} {str(bit)}")# se manda a escribir al hub que le llega o recibe el bit correspondiente
            if isinstance(actual_device,Switch):
                ports_to_send=actual_device.send_port(net,v[0])#pide al switch por los puertos que va a enviar
                queue.append([ p for p in ports_to_send])#agrega a la cola todos los puertos por los que va a enviar el switch

    @staticmethod
    def comprobate_net(net:Net,bit:int,time:int,u,v,queue:list,visited:dict,collisions:list,ports_tree:list):
        actual_device = net.my_device(v[0])
        ports_tree.append(v[0])


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




