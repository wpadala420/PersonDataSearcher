import networkx as nx
import matplotlib.pyplot as plt


class GraphVisualization:

    def __init__(self):
        self.visual = []

    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)

    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.savefig("simple_path.png")
        # plt.show()


G = GraphVisualization()
for i in range(250):
    G.addEdge('wojtek', 'wojtek' + str(i))

G.visualize()