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
        plt.figure(figsize=(30, 30))
        nx.draw_networkx(G)
        plt.tight_layout()
        plt.savefig("simple_path.png", dpi=300)
        # plt.show()


G = GraphVisualization()
for i in range(250):
    G.addEdge('wojtek', 'wojtek' + str(i))

G.visualize()