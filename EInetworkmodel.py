import random as r
import numpy as np
import math as m
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import singleneuronmodel as snm
import networkmodel as nm

#Generating random soma in the space [-x,x]x[-y,y]
def generateEISoma(mu,x_range,y_range,EIprop):
    area = (y_range[1]-y_range[0])*(x_range[1]-x_range[0])
    numberOfSoma = np.random.poisson(mu*area)
    #Distributing the soma randomly in space
    x_pos=np.random.uniform(x_range[0],x_range[1],numberOfSoma)
    y_pos=np.random.uniform(y_range[0],y_range[1],numberOfSoma)
    soma =[]
    for i in range(0,numberOfSoma):
        EI=np.random.uniform(0,1)
        if EI>EIprop:
            EItype="E"
        else:
            EItype="I"
        soma.append([x_pos[i],y_pos[i],EItype])
    return([soma,x_pos,y_pos])

#Growing a random EI network
def growRandomEINetwork(mu,x_range,y_range,angle_lowerbound,angle_upperbound,T,lamb,radius,EIprop):
    soma = generateEISoma(mu,x_range,y_range,EIprop)
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
    for v in somaPositions:
        edges=snm.growingneuron(angle_lowerbound,angle_upperbound,T,lamb,v[:2])
        trees.append(edges)

    adjacencyMatrix =[]

    for v in somaPositions:
        v_connections =[]
        for tree in trees:
            if nm.are_vtx_connected(tree,v,radius):
                v_connections.append(1)
            else:
                v_connections.append(0)
        adjacencyMatrix.append(v_connections)

    for i in range(0,len(somaPositions)):
        #remove self connections
        adjacencyMatrix[i][i]=0
    #transpose the matrix (as we built the transpose)
    adjacencyMatrix = np.array(adjacencyMatrix).T.tolist()
    return([adjacencyMatrix,somaPositions])