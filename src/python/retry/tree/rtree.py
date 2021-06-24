"""
"ReTry" (c) by Ignacio Slater M.
"ReTry" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <https://creativecommons.org/licenses/by/4.0/>.
"""
import math

import matplotlib.pyplot as plt
from retry.tree.internal import NodeDirectory
from retry.tree.leaf import NodeLeaf, RegisterEntry


class RTree:
    def __init__(self, m, M):
        self.m = m
        self.M = M
        self.root = NodeLeaf(self.m, self.M)

    def insert(self, point):

        result = self.root.insertPoint(point)

        if result[0] == True:
            flag, L, LL, R1, R2 = result

            newNode = NodeDirectory(self.m, self.M)

            if isinstance(self.root, NodeLeaf):
                node1 = NodeLeaf(self.m, self.M)
                node2 = NodeLeaf(self.m, self.M)
            else:
                node1 = NodeDirectory(self.m, self.M)
                node2 = NodeDirectory(self.m, self.M)

            node1.storage = L
            node2.storage = LL

            newNode.storage.append(RegisterEntry(R1, node1))
            newNode.storage.append(RegisterEntry(R2, node2))

            self.root = newNode

    def range_search(self, rect):
        return self.root.range_search(rect)

    def range_search2(self, point, radius):
        return self.root.range_search2(point, radius)

    def nearest_neighbor_depth(self, point):
        (dist, neighbor, numNodes) = self.root.nearest_neighbor_depth(point, resultdist=math.inf,
                                                                      num_nodes=0)
        return (dist, neighbor, numNodes)

    def nnRKV(self, point):
        pass

    def __str__(self):
        return self.root.__str__()

    def draw(self, width, height):
        ax = plt.gca()
        ax.set_xlim(-5, width + 5)
        ax.set_ylim(-5, height + 5)

        self.root.draw(ax)
        plt.show()
