import random as r
import numpy as np
import math as m
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import singleneuronmodel as snm

def makeGraph(Network):
    adj = Network[0]
    nodeInfo = Network[1]
    N=len(adj)
    G = nx.DiGraph()
    for i in range(0,N):
        G.add_node(i,pos=(nodeInfo[1][i],nodeInfo[2][i]))
        for j in range(0,N): 
                if adj[i][j] == 1: 
                    G.add_edge(i,j)
    return(G)

def plotGraph(G):
    nx.draw(G,nx.get_node_attributes(G, 'pos'),with_labels=False)

def circlePlotGraph(G):
    nx.draw_circular(G)
    plt.savefig('HN.png', bbox_inches='tight')
    plt.show()

def averageDegree(G):
    K = 0
    for node in G.nodes():
        K+=G.degree(node)
    return(K/G.number_of_nodes())

def basicAnalysisGraph(G):
    print("Nodes: " + str(G.number_of_nodes()))
    print("Edges: " + str(G.number_of_edges()))
    print("Average degree: " + str(averageDegree(G)))

def plotDegreeDistribution(G):
    degrees = [G.degree(n) for n in G.nodes()]
    plt.hist(degrees)
    plt.xlabel('Degree')
    plt.ylabel('Freq. density')
    plt.show()