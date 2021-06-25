"""
"ReTry" (c) by Ignacio Slater M.
"ReTry" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <https://creativecommons.org/licenses/by/4.0/>.
"""
import math

import matplotlib.pyplot as plt
from retry.geometry import Point
from retry.tree.commons import RegisterEntry
from retry.tree.inner import NodeDirectory
from retry.tree.leaf import NodeLeaf


class RTree:
    def __init__(self, m1, m2):
        self.m1 = m1
        self.m2 = m2
        self.root = NodeLeaf(self.m1, self.m2)

    def insert(self, point):

        result = self.root.insertPoint(point)

        if result[0]:
            flag, l, ll, r1, r2 = result

            new_node = NodeDirectory(self.m1, self.m2)

            if isinstance(self.root, NodeLeaf):
                node1 = NodeLeaf(self.m1, self.m2)
                node2 = NodeLeaf(self.m1, self.m2)
            else:
                node1 = NodeDirectory(self.m1, self.m2)
                node2 = NodeDirectory(self.m1, self.m2)

            node1.storage = l
            node2.storage = ll

            new_node.storage.append(RegisterEntry(r1, node1))
            new_node.storage.append(RegisterEntry(r2, node2))

            self.root = new_node

    def range_search(self, rect):
        return self.root.range_search(rect)

    def range_search2(self, point, radius):
        return self.root.range_search2(point, radius)

    def nearest_neighbor_depth(self, point):
        (dist, neighbor, numNodes) = self.root.nearest_neighbor_depth(point, resultdist=math.inf,
                                                                      num_nodes=0)
        return dist, neighbor, numNodes

    def nnRKV(self, point: Point):
        return self.root.nn_rkv(point, math.inf, math.inf, 0)

    def __str__(self):
        return self.root.__str__()

    def draw(self, width, height):
        ax = plt.gca()
        ax.set_xlim(-5, width + 5)
        ax.set_ylim(-5, height + 5)

        self.root.draw(ax)
        plt.show()
