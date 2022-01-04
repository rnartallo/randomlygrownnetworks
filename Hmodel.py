import random as r
import numpy as np
import math as m
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import singleneuronmodel as snm
import networkmodel as nm
import EInetworkmodel as ei


def growRandomHopfieldNetwork(mu,x_range,y_range,angle_lowerbound,angle_upperbound,T,lamb,radius):
    soma = nm.generateSoma(mu,x_range,y_range)
    plt.scatter(soma[1],soma[2])
    trees =[]
    somaPositions = soma[0]
    N = len(somaPositions)
    for v in somaPositions:
        edges=snm.growingneuron(angle_lowerbound,angle_upperbound,T,lamb,v)
        trees.append(edges)

    adjacencyMatrix = np.zeros(shape=(N,N))

    for i in range(0,N):
        for j in range(0,N):
            if adjacencyMatrix[i][j]==0:
                if nm.are_vtx_connected(trees[j],somaPositions[i],radius):
                    adjacencyMatrix[i][j]=1
                    adjacencyMatrix[j][i]=1

    for i in range(0,N):
        #remove self connections
        adjacencyMatrix[i][i]=0
    adjacencyMatrix = adjacencyMatrix.tolist()
    return([adjacencyMatrix,soma])

def growRandomEIHopfieldNetwork(mu,x_range,y_range,angle_lowerbound,angle_upperbound,T,lamb,radius,EIprop):
    soma = ei.generateEISoma(mu,x_range,y_range,EIprop)
    xpos=soma[1]
    ypos=soma[2]
    somaInfo=soma[0]
    for i in range(0,len(xpos)):
        if somaInfo[i][2]=="I":
            plt.scatter(xpos[i],ypos[i],color="orange")
        else:
            plt.scatter(xpos[i],ypos[i],color="black")

    trees =[]
    somaPositions = soma[0]
    N = len(somaPositions)

    for v in somaPositions:
        edges=snm.growingneuron(angle_lowerbound,angle_upperbound,T,lamb,v[:2])
        trees.append(edges)

    adjacencyMatrix = np.zeros(shape=(N,N))

    for i in range(0,N):
        for j in range(0,N):
            if adjacencyMatrix[i][j]==0:
                if nm.are_vtx_connected(trees[j],somaPositions[i],radius):
                    adjacencyMatrix[i][j]=1
                    adjacencyMatrix[j][i]=1
                    
    for i in range(0,len(somaPositions)):
        #remove self connections
        adjacencyMatrix[i][i]=0
    adjacencyMatrix = adjacencyMatrix.tolist()
    return([adjacencyMatrix,somaPositions])

def circlePlotColourGraph(G,colour_map):
    nx.draw_circular(G,node_color=colour_map, with_labels=False)
    plt.show()