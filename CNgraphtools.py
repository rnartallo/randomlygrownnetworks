import random as r
import numpy as np
import math as m
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import singleneuronmodel as snm
import networkmodel as nm
import mynetworkx as my_nx

def areClustersConnected(i,j,Network):
    adj=Network[0]
    nodeInfo=Network[1]
    for n in range(0,len(nodeInfo)):
        if nodeInfo[n][3]==i:
            for m in range(0,len(adj)):
                if adj[n][m]==1:
                    if nodeInfo[m][3]==j:
                        return(True)
    return(False)

def countClusterConnections(i,j,Network):
    adj=Network[0]
    nodeInfo=Network[1]
    c=0
    for n in range(0,len(nodeInfo)):
        if nodeInfo[n][3]==i:
            for m in range(0,len(adj)):
                if adj[n][m]==1:
                    if nodeInfo[m][3]==j:
                        c+=1
    return(c)

def ClusterGraph(Network):
    adj=Network[0]
    nodeInfo=Network[1]
    n = nodeInfo[len(nodeInfo)-1][3]
    clusterAdj =[]
    for i in range(1,n+1):
        clusterConnections=[]
        for j in range(1,n+1):
            if areClustersConnected(i,j,Network):
                clusterConnections.append(1)
            else:
                clusterConnections.append(0)
        clusterAdj.append(clusterConnections)
    #Remove self connections
    for i in range(0,n):
        clusterAdj[i][i]=0
    return(clusterAdj)

def WeightedClusterGraph(Network):
    adj=Network[0]
    nodeInfo=Network[1]
    n = nodeInfo[len(nodeInfo)-1][3]
    clusterAdj =[]
    for i in range(1,n+1):
        clusterConnections=[]
        for j in range(1,n+1):
            clusterConnections.append(countClusterConnections(i,j,Network))
        clusterAdj.append(clusterConnections)
    #Remove self connections
    for i in range(0,n):
        clusterAdj[i][i]=0
    return(clusterAdj)

def makeClusterGraph(adj):
    G = nx.DiGraph()
    G.add_node(1, pos=(1, 3))
    G.add_node(2, pos=(3, 3))
    G.add_node(3, pos=(2, 2))
    G.add_node(4, pos=(1, 1))
    G.add_node(5, pos=(3, 1))
    for i in range(0,len(adj)):
        for j in range(0,len(adj)):
            if adj[i][j]==1:
                G.add_edge(i+1,j+1)
    nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, node_size=1000)
    plt.show()
    return(G)

def makeWeightedClusterGraph(adj):
    G = nx.DiGraph()
    G.add_node(1, pos=(1, 3))
    G.add_node(2, pos=(3, 3))
    G.add_node(3, pos=(2, 2))
    G.add_node(4, pos=(1, 1))
    G.add_node(5, pos=(3, 1))
    for i in range(0,len(adj)):
        for j in range(0,len(adj)):
            if adj[i][j]>0:
                G.add_edge(i+1,j+1,weight=adj[i][j])
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos)
    curved_edges = [edge for edge in G.edges() if reversed(edge) in G.edges()]
    straight_edges = list(set(G.edges()) - set(curved_edges))
    nx.draw_networkx_edges(G, pos, edgelist=straight_edges)
    arc_rad = 0.1
    nx.draw_networkx_edges(G, pos, edgelist=curved_edges, connectionstyle=f'arc3, rad = {arc_rad}')
    edge_weights = nx.get_edge_attributes(G,'weight')
    curved_edge_labels = {edge: edge_weights[edge] for edge in curved_edges}
    straight_edge_labels = {edge: edge_weights[edge] for edge in straight_edges}
    my_nx.my_draw_networkx_edge_labels(G, pos, edge_labels=curved_edge_labels,rotate=False,rad = arc_rad)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=straight_edge_labels,rotate=False)
    plt.savefig('weightedclustergraph.png', bbox_inches='tight')
    plt.show()
    return(G)

def makeColourHyperGraphLocProj(Network):
    adj = Network[0]
    nodeInfo = Network[1]
    colour_map =[]
    G = nx.DiGraph()
    for i in range(0,len(nodeInfo)):
        G.add_node(i,pos=(nodeInfo[i][0],nodeInfo[i][1]))
        if nodeInfo[i][2]=="Inter":
            colour_map.append("green")
        else:
            colour_map.append("red")
        for j in range(0,len(nodeInfo)): 
            if adj[i][j] == 1: 
                G.add_edge(i,j)
    return([G,colour_map])

def plotColourGraph(G,colour_map):
    nx.draw(G,nx.get_node_attributes(G, 'pos'),node_color=colour_map, with_labels=False)
    plt.show()

def LocProjGraphNumberOfNodes(Network):
    nodeInfo=Network[1]
    proj=0
    inter=0
    print("Neurons: " + str(len(nodeInfo)))
    for i in range(0,len(nodeInfo)):
        if nodeInfo[i][2]=="Inter":
            inter+=1
        else:
            proj+=1
    print("Projectory Neurons: "+ str(proj))
    print("Interneurons: " + str (inter))

def calculateLocProjDegreeDistribution(Network):
    loc_degrees = []
    proj_degrees = []
    adj = Network[0]
    G=makeColourHyperGraphLocProj(Network)[0]
    nodeInfo = Network[1]
    for i in range(0,len(nodeInfo)):
        if nodeInfo[i][2]=="Inter":
            loc_degrees.append(G.degree(i))
        else:
            proj_degrees.append(G.degree(i))
    return([loc_degrees,proj_degrees])

def plotLocProjDegreeDistribution(loc_degrees,proj_degrees):
    plt.hist(loc_degrees, alpha =0.7,label="Interneurons",color="green")
    plt.hist(proj_degrees,alpha=0.5, label="Projectory Neurons",color ="red")
    plt.xlabel("Degree")
    plt.ylabel("Frequency density")
    plt.legend(loc='upper right')
    plt.show()

def calculateProjectoryDegree(Network):
    adj = Network[0]
    nodeInfo= Network[1]
    degrees = [0]*len(nodeInfo)
    for i in range(0,len(nodeInfo)):
        for j in range(0,len(nodeInfo)):
            if adj[i][j]==1:
                if nodeInfo[j][3]!=nodeInfo[i][3]:
                    degrees[i]+=1
    return(degrees)

def calculateLocProjProjectoryDegreeDistribution(Network,degrees):
    loc_degrees = []
    proj_degrees = []
    adj = Network[0]
    G=makeColourHyperGraphLocProj(Network)[0]
    nodeInfo = Network[1]
    for i in range(0,len(nodeInfo)):
        if nodeInfo[i][2]=="Inter":
            loc_degrees.append(degrees[i])
        else:
            proj_degrees.append(degrees[i])
    return([loc_degrees,proj_degrees])