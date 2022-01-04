import random as r
import numpy as np
import math as m
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import singleneuronmodel as snm
import networkmodel as nm

#Generating random soma in the space [-x,x]x[-y,y]

def generateLocProjSoma(inter_mu,proj_mu,x_range,y_range):
    area = (y_range[1]-y_range[0])*(x_range[1]-x_range[0])
    numberOfInterSoma = np.random.poisson(inter_mu*area)
    numberOfProjSoma = np.random.poisson(proj_mu*area)
    #Distributing the soma randomly in space
    inter_x_pos=list(np.random.uniform(x_range[0],x_range[1],numberOfInterSoma))
    inter_y_pos=list(np.random.uniform(y_range[0],y_range[1],numberOfInterSoma))
    proj_x_pos=list(np.random.uniform(x_range[0],x_range[1],numberOfProjSoma))
    proj_y_pos=list(np.random.uniform(y_range[0],y_range[1],numberOfProjSoma))
    x_pos=np.array(inter_x_pos+proj_x_pos)
    y_pos=np.array(inter_y_pos+proj_y_pos)
    soma =[]
    for i in range(0,numberOfInterSoma):
        soma.append([inter_x_pos[i],inter_y_pos[i],"Inter"])
    for i in range(0,numberOfProjSoma):
        soma.append([proj_x_pos[i],proj_y_pos[i],"Proj"])
    return([soma,x_pos,y_pos])

def generateClusteredLocProjSoma(inter_mu,proj_mu,x_range,y_range):
    x_dist = x_range[1]-x_range[0]
    y_dist = y_range[1]-y_range[0]
    clusters =[]
    clusters.append(generateLocProjSoma(inter_mu,proj_mu,[x_range[0],x_range[0]+x_dist/3],[y_range[1]-y_dist/3,y_range[1]]))
    clusters.append(generateLocProjSoma(inter_mu,proj_mu,[x_range[1]-x_dist/3,x_range[1]],[y_range[1]-y_dist/3,y_range[1]]))
    clusters.append(generateLocProjSoma(inter_mu,proj_mu,[x_range[0]+x_dist/3,x_range[1]-x_dist/3],[y_range[0]+y_dist/3,y_range[1]-y_dist/3]))
    clusters.append(generateLocProjSoma(inter_mu,proj_mu,[x_range[0],x_range[0]+x_dist/3],[y_range[0],y_range[0]+y_dist/3]))
    clusters.append(generateLocProjSoma(inter_mu,proj_mu,[x_range[1]-x_dist/3,x_range[1]],[y_range[0],y_range[0]+y_dist/3]))
    return(clusters)

def growRandomClusteredLocProjNetwork(inter_mu,proj_mu,x_range,y_range,angle_lowerbound,angle_upperbound,T,inter_lamb,proj_lamb,radius):
    clusters = generateClusteredLocProjSoma(inter_mu,proj_mu,x_range,y_range)
    loctrees =[]
    projtrees=[]
    trees=[]
    for c in clusters:
        xpos=c[1]
        ypos=c[2]
        soma=c[0]
        for i in range(0,len(xpos)):
            if soma[i][2]=="Inter":
                plt.scatter(xpos[i],ypos[i],color="green")
                edges=snm.growingneuron(angle_lowerbound,angle_upperbound,T,inter_lamb,[xpos[i],ypos[i]])
                loctrees.append(edges)
            else:
                plt.scatter(xpos[i],ypos[i],color="red")
                edges=snm.growingneuron(angle_lowerbound,angle_upperbound,T,proj_lamb,[xpos[i],ypos[i]])
                projtrees.append(edges)
            trees.append(edges)

    adjacencyMatrix =[]
    somaPos=[]
    for c in clusters:
        somaPositions = c[0]
        for s in somaPositions:
            s.append(clusters.index(c)+1)
        somaPos.extend(somaPositions)
        for v in somaPositions:
            v_connections =[]
            for tree in trees:
                if nm.are_vtx_connected(tree,v,radius):
                    v_connections.append(1)
                else:
                    v_connections.append(0)
            adjacencyMatrix.append(v_connections)

    for i in range(0,len(adjacencyMatrix)):
        #remove self connections
        adjacencyMatrix[i][i]=0
    #transpose the matrix (as we built the transpose)
    adjacencyMatrix = np.array(adjacencyMatrix).T.tolist()
    return([adjacencyMatrix,somaPos])