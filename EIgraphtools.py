import random as r
import numpy as np
import math as m
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import singleneuronmodel as snm
import networkmodel as nm
import copy

def starExpansion(EINetwork):
    adjMatrix = copy.deepcopy(EINetwork[0])
    somaPositions = EINetwork[1]
    for j in range(0,len(somaPositions)):
        if somaPositions[j][2]=="E":
            adjMatrix[j].append(1)
            adjMatrix[j].append(0)
        else:
            adjMatrix[j].append(0)
            adjMatrix[j].append(1)            
    adjMatrix.append([0] * (len(somaPositions)+2))
    adjMatrix.append([0] * (len(somaPositions)+2))
    return(adjMatrix)

def makeColourHyperGraph(Network):
    adj = Network[0]
    nodeInfo = Network[1]
    colour_map =[]
    G = nx.DiGraph() 
    for i in range(0,len(nodeInfo)):
        G.add_node(i,pos=(nodeInfo[i][0],nodeInfo[i][1]))
        if nodeInfo[i][2]=="I":
            colour_map.append("orange")
        else:
            colour_map.append("black")
        for j in range(0,len(nodeInfo)): 
            if adj[i][j] == 1: 
                G.add_edge(i,j)
    return([G,colour_map])

def plotColourGraph(G,colour_map):
    nx.draw(G,nx.get_node_attributes(G, 'pos'),node_color=colour_map, with_labels=False)
    plt.show()
    
def plotStarGraph(adj):
    #Graph tools
    N=len(adj)
    G = nx.DiGraph()
    for i in range(0,N):
        for j in range(0,N): 
            if adj[i][j] == 1: 
                G.add_edge(i,j)
    N = G.number_of_nodes()
    color_map = []
    for node in G:
        if node == N-1:
            color_map.append("orange")
        elif node == N-2:
            color_map.append("black")
        else:
            color_map.append("blue")
    nx.draw_networkx(G,node_color = color_map,pos = nx.drawing.layout.bipartite_layout(G, [N-2,N-1]),with_labels = False)
    return(G)

def EIGraphNumberOfNodes(G):
    N=G.number_of_nodes()
    print("Nodes: " + str(N))
    print("Neurons: " + str(N-2))
    print("Excitory: " + str(G.degree(N-2)))
    print("Inhibitory: " + str(G.degree(N-1)))

def calculateEIDegreeDistribution(Network):
    inh_degrees = []
    exc_degrees = []
    adj = Network[0]
    G=makeColourHyperGraph(Network)[0]
    nodeInfo = Network[1]
    for i in range(0,len(nodeInfo)):
        if nodeInfo[i][2]=="I":
            inh_degrees.append(G.degree(i))
        else:
            exc_degrees.append(G.degree(i))
    return([inh_degrees,exc_degrees])

def plotEIDegreeDistribution(inh_degrees,exc_degrees):
    plt.hist(inh_degrees, alpha =0.7,label="Inhibitory",color="orange")
    plt.hist(exc_degrees,alpha=0.5, label="Excitory",color ="grey")
    plt.xlabel('Degree')
    plt.ylabel('Freq. density')
    plt.legend(loc='upper right')
    plt.show()