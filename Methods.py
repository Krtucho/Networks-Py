from Graph import Graph
from Port import Port
from Device import Device
from Hub import Hub
from Host import Host
from Queue import queue

# def BFS00(graph:Graph,s:Port):
#     queue=[]
#     d={}
#     i:int
#     #i=0
#     queue.append(s)
#     while queue.count>0:
#         u=queue.pop()
#         for v in graph.E[u]:
#             if d[v] == 0:
#                 d[v]=d[u]+1
#                 queue.enqueue(v)
    
#     return d

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

# def instruction_parser(graph:Graph,list:[]):
#     if list[1]== "create":
#         if list[2]=="hub":
#             graph.add_vertex(Hub(list[3],list[4]))
#         else :
#             if list[2]=="host":
#                 graph.add_vertex(Host(list[3]))
#         return
#     if list[1]== "connect":
#         graph.add_edge(list[2],list[3],none)
#         return    

#     if list[1]== "disconnect":
#         graph.remove_edge(list[2])

#     if list[1]== "send":
#         pass#implementar








graph=Graph()
graph.add_vertex(Host("pc1"))
graph.add_vertex(Hub("h1",4))
graph.add_vertex(Host("pc2"))
graph.add_vertex(Host("h2",4))






        







