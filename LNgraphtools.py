import random as r
import numpy as np
import math as m
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import singleneuronmodel as snm
import networkmodel as nm

def calculateNumberOfLayers(Network):
    n=0
    for node in Network[1]:
        if node[2]>n:
            n=node[2]
    return(n)

def organiseLayers(Network):
    adj = Network[0]
    noLayers = calculateNumberOfLayers(Network)
    nodeInfo = Network[1]
    G = nx.DiGraph()
    Layers = [[] for x in range(noLayers)]
    for i in range(0,len(nodeInfo)):
        Layers[nodeInfo[i][2]-1].append(nodeInfo[i])
    return(Layers)

def sortLayersByYPos(layers):
    sortedLayers=[]
    for layer in layers:
        sortedLayers.append(sorted(layer, key = lambda x: x[1]))
    return(sortedLayers)

def makeLayeredGraph(Network):
    adj=Network[0]
    nodeInfo=Network[1]
    layers = sortLayersByYPos(organiseLayers(Network))
    G = nx.DiGraph()
    for i in range(0,len(nodeInfo)):
        node = nodeInfo[i]
        layer = layers[node[2]-1]
        positionInLayer = layer.index(node)
        G.add_node(i,pos=(2*(node[2]),2*positionInLayer))
        for j in range(0,len(nodeInfo)):
            if adj[i][j]==1:
                G.add_edge(i,j)
    return(G)
        
def plotLayeredGraph(G):
    nx.draw(G,nx.get_node_attributes(G, 'pos'), with_labels=False)
    plt.show()

def findDisconnectedNodes(Network):
    noLayers = calculateNumberOfLayers(Network)
    adj=Network[0]
    nodeInfo=Network[1]
    unconnectedNodes =[]
    for i in range(0,len(nodeInfo)):
        connected = False
        if nodeInfo[i][2]==noLayers or nodeInfo[i][2]==1: #Do not remove output or input layers
            connected = True
        for j in range(0,len(nodeInfo)):
            if adj[i][j]==1:
                connected = True
        if not connected:
            unconnectedNodes.append(i)
    return(unconnectedNodes)

def removeDisconnectedNodes(Network):
    unconnectedNodes=sorted(findDisconnectedNodes(Network))
    adj=Network[0]
    nodeInfo=Network[1]
    for i in range(0,len(unconnectedNodes)):
        adj = np.delete(adj,unconnectedNodes[i]-i,axis=1)
        adj = np.delete(adj,unconnectedNodes[i]-i,axis=0)
        nodeInfo.pop(unconnectedNodes[i]-i)
    return([adj,nodeInfo])

def findUnusedNodes(Network):
    noLayers = calculateNumberOfLayers(Network)
    adj=Network[0]
    nodeInfo=Network[1]
    unusedNodes =[]
    for i in range(0,len(nodeInfo)):
        used = False
        if nodeInfo[i][2]==noLayers or nodeInfo[i][2]==1: #Do not remove output or input layers
            used = True
        for j in range(0,len(nodeInfo)):
            if adj[j][i]==1:
                used = True
        if not used:
            unusedNodes.append(i)
    return(unusedNodes)

def removeUnusedNodes(Network):
    unusedNodes=sorted(findUnusedNodes(Network))
    adj=Network[0]
    nodeInfo=Network[1]
    for i in range(0,len(unusedNodes)):
        adj = np.delete(adj,unusedNodes[i]-i,axis=1)
        adj = np.delete(adj,unusedNodes[i]-i,axis=0)
        nodeInfo.pop(unusedNodes[i]-i)
    return([adj,nodeInfo])