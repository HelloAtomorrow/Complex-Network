#partition = community.best_partition(User)
import networkx as nx
import matplotlib.pyplot as plt
import operator
import copy
from functools import reduce
from time import clock

#生成一个随机图
def CreatRandomPicture():
    #G = nx.random_graphs.barabasi_albert_graph(20,1)
    G = nx.random_graphs.erdos_renyi_graph(5, 0.5)
    #print(G.nodes())
    #print(G.edges())
    #画图
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_size=10)
    plt.savefig("RandomPicture.png")
    return G

#计算连边相似度
def LinkSimilarity(node, edge):
    print('lenth of node: ' + str(len(node)))
    print('lenth of edge: ' + str(len(edge)))
    data_link_similarity = []
    for i in range(0, len(edge)):
        for j in range(i + 1, len(edge)):
            node_one_neighbor = []
            node_two_neighbor = []
            if (((sorted(edge[i])) != (sorted(edge[j]))) and (len(set(edge[i]) & set(edge[j]))) != 0):
                common = set(edge[i]) & set(edge[j])
                node_one = set(edge[i]) ^ set(common)
                node_two = set(edge[j]) ^ set(common)

                for x in range(0, len(edge)):
                    if (set(edge[x]) & set(node_one)):
                        node_one_neighbor.append(list(set(edge[x]) ^ node_one)[0])
                    if (set(edge[x]) & set(node_two)):
                        node_two_neighbor.append(list(set(edge[x]) ^ node_two)[0])

                node_one_neighbor.append(list(node_one)[0])
                node_two_neighbor.append(list(node_two)[0])

                node_jiao = set(node_one_neighbor) & set(node_two_neighbor)
                node_bing = set(node_one_neighbor).union(set(node_two_neighbor))

                ls = len(node_jiao) / len(node_bing)

                link_similarity = []
                link_similarity.append(list(node_one)[0])
                link_similarity.append(list(common)[0])
                link_similarity.append(list(node_two)[0])
                link_similarity.append(ls)
                data_link_similarity.append(link_similarity)
    #降序排列连边相似度
    data_link_similarity = sorted(data_link_similarity, key=lambda x:x[3], reverse=True)
    return data_link_similarity

#计算划分密度
def ComputeDensity(data_community):
    D = 0.0
    M = 0
    for community in data_community:
        mc = len(community)
        M += mc
        node = []
        for each_edge in community:
            node.append(each_edge[0])
            node.append(each_edge[1])
        node = set(node)
        nc = len(node)
        #print(mc, nc)
        if nc == 2:
            continue
        else:
            D += (mc * (mc - (nc - 1))) / ((nc - 2) * (nc - 1))
    D = 2 * D / M
    print('D: ', D)
    return D


#社团合并
def CombineCommunity(data_link_similarity):
    D_old = 0
    data_community = []
    #初始时每条边为一个社团
    for each_edge in edge:
        data_community.append([each_edge])
    print(data_community)
    for link in data_link_similarity:
        cm0 = list()
        cm1 = list()
        for community in data_community:
            if ((link[0], link[1]) in community) or ((link[1], link[0]) in community):
                cm0 = community
            if ((link[1], link[2]) in community) or ((link[2], link[1]) in community):
                cm1 = community
        if cm0 in data_community:
            data_community.remove(cm0)
        if cm1 in data_community:
            data_community.remove(cm1)
        #print(cm0, cm1)
        cm = cm0 + cm1
        # 对cm去重
        temp = []
        for each_edge in cm:
            if each_edge not in temp:
                temp.append(each_edge)
        data_community.append(temp)

        D = ComputeDensity(data_community)
        #print(data_community)
        if D >= D_old:
            D_old = D
            continue
        else:
            #输出上一个状态的社团划分结果
            data_community.remove(temp)
            data_community.append(cm0)
            data_community.append(cm1)
            return data_community
    return data_community

G = CreatRandomPicture()

node = []
edge = []
for e in G.edges():
    x = e[0]
    y = e[1]
    edge.append((x, y))
for i in range(0,len(edge)):
    node += set(edge[i])
node = set(node)

data_link_similarity = LinkSimilarity(node, edge)
print(data_link_similarity)

data_community = CombineCommunity(data_link_similarity)

#将社团中的边变换为点
data_community_node = []
for community in data_community:
    community_node = set()
    for each_edge in community:
        community_node.add(each_edge[0])
        community_node.add(each_edge[1])
    data_community_node.append(community_node)

print(data_community_node)

