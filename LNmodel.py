import random as r
import numpy as np
import math as m
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import singleneuronmodel as snm
import networkmodel as nm

def distributeFirstLayer(soma,inputLayer):
    input_x_pos=list(np.random.uniform(0,2,inputLayer))
    input_y_pos=list(np.random.uniform(0,8,inputLayer))
    for i in range(0,inputLayer):
        soma.append([input_x_pos[i],input_y_pos[i],1])
    return(soma)

def distributeOutputLayer(soma,outputLayer,noLayers):
    output_x_pos=list(np.random.uniform(2*(noLayers-1),2*noLayers,outputLayer))
    output_y_pos=list(np.random.uniform(0,8,outputLayer))
    for i in range(0,outputLayer):
        soma.append([output_x_pos[i],output_y_pos[i],noLayers])
    return(soma)

def distributeHiddenLayers(soma,mu,noLayers):
    for i in range(1,noLayers-1):
        no_nodes = np.random.poisson(mu*16)
        x_pos=list(np.random.uniform(2*i,2*(i+1),no_nodes))
        y_pos=list(np.random.uniform(0,8,no_nodes))
        for j in range(0,no_nodes):
            soma.append([x_pos[j],y_pos[j],i+1])
    return(soma)

def growRandomLayeredNetwork(mu,inputLayer,outputLayer,noLayers,angle_lowerbound,angle_upperbound,T,lamb,radius):
    soma = distributeFirstLayer([],inputLayer)
    soma = distributeOutputLayer(soma,outputLayer,noLayers)
    soma = distributeHiddenLayers(soma,mu,noLayers)
    trees=[]
    for i in range(0,len(soma)):
        plt.scatter(soma[i][0],soma[i][1],color="black")
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