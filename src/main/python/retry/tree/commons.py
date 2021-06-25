"""
"ReTry" (c) by Ignacio Slater M.
"ReTry" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <https://creativecommons.org/licenses/by/4.0/>.
"""
from abc import ABCMeta, abstractmethod


class Node(metaclass=ABCMeta):
    @abstractmethod
    def nn_rkv(self, point, result_dist, pruning_dist, num_nodes):
        """
        Calculates the nearest neighbour of a point using the RKV algorithm ("Nearest Neighbor
        Queries", Roussopouls et. al. 1995)
        """
        pass

    @abstractmethod
    def nearest_neighbor_depth(self, point, resultdist, num_nodes):
        pass


class RegisterEntry:
    """
    Class to store an individual record of the R-Tree. It contains a geometric object (point or
    rect) and a pointer to a Node
    """

    def __init__(self, geo_object, pointer: Node):
        self.object = geo_object
        self.pointer = pointer
