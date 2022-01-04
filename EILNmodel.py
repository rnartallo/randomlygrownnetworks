import random as r
import numpy as np
import math as m
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import singleneuronmodel as snm
import networkmodel as nm
import LNmodel as ln

def distributeEI(soma,EIprop):
    for i in range(0,len(soma)):
        EI=np.random.uniform(0,1)
        if EI>EIprop:
            EItype="E"
        else:
            EItype="I"
        soma[i].append(EItype)
    return(soma)

def makeColourMap(somaInfo):
    colour_map =[]
    for soma in somaInfo:
        if soma[3] == "E":
            colour_map.append("black")
        else:
            colour_map.append("orange")
    return(colour_map)

def plotColouredLayeredGraph(G,colour_map):
    nx.draw(G,nx.get_node_attributes(G, 'pos'),node_color =colour_map, with_labels=False)
    plt.show()

def growRandomEILayeredNetwork(mu,inputLayer,outputLayer,noLayers,angle_lowerbound,angle_upperbound,T,lamb,radius,EIprop):
    soma = ln.distributeFirstLayer([],inputLayer)
    soma = ln.distributeOutputLayer(soma,outputLayer,noLayers)
    soma = ln.distributeHiddenLayers(soma,mu,noLayers)
    soma = distributeEI(soma,EIprop)
    trees=[]
    for i in range(0,len(soma)):
        if soma[i][3]=="E":
            plt.scatter(soma[i][0],soma[i][1],color="black")
        else:
            plt.scatter(soma[i][0],soma[i][1],color="orange")
        edges=snm.growingneuron(angle_lowerbound,angle_upperbound,T,lamb,[soma[i][0],soma[i][1]])
        trees.append(edges)
    adjMatrix =[]
    for i in range(0,len(soma)):
        connections =[]
        v=[soma[i][0],soma[i][1]]
        for j in range(0,len(trees)):
            if nm.are_vtx_connected(trees[j],v,radius):
                if soma[j][2]==soma[i][2]-1:
                    connections.append(1)
                else:
                    connections.append(0)
            else:
                connections.append(0)
        adjMatrix.append(connections)
    
    #For the output layer which has no connections
    for i in range(0,len(adjMatrix)):
        #remove self connections
        adjMatrix[i][i]=0
    #transpose the matrix (as we built the transpose)
    adjMatrix = np.array(adjMatrix).T.tolist()
    return([adjMatrix,soma])