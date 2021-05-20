import networkx as nx
import matplotlib.pyplot as plt
import modules.Person


class GraphVisualization:

    def __init__(self):
        self.visual = []

    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)

    def visualize(self, filename):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        plt.figure(figsize=(40, 40))
        nx.draw_networkx(G)
        plt.tight_layout()
        plt.savefig(filename, dpi=150)
        # plt.show()
