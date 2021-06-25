"""
"ReTry" (c) by Ignacio Slater M.
"ReTry" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <https://creativecommons.org/licenses/by/4.0/>.
"""
from typing import Tuple

from retry.geometry import Point, Rect
from retry.tree.commons import Node, RegisterEntry

ResultDist: float


# Class to store a leaf node
# It stores the parameters of the structure and a collection of RegisterEntry
class NodeLeaf(Node):
    def __init__(self, m, M):
        self.m = m
        self.M = M
        self.storage = []  # collection of registerEntry

    # Insert a point in a leaf node
    def insertPoint(self, point):
        if len(self.storage) < self.M:  # Point fits in node
            self.storage.append(RegisterEntry(point, None))
            return (False, None)  # Store and return False (there is no split)

        # Point does not fit in node, split
        L, LL, rect1, rect2 = self.split(point)

        return (True, L, LL, rect1, rect2)  # Returns True and the information about the split

    # Method for 'print'
    def __str__(self):
        auxStr = "| "
        for elem in self.storage:
            auxStr = auxStr + f"{elem.object.__str__()} | "

        return auxStr

    def draw(self, ax):
        for elem in self.storage:
            elem.object.draw(ax)

    def range_search(self, rect):
        resultList = []

        for elem in self.storage:
            if rect.is_point_in_rectangle(elem.object):
                resultList.append(elem.object)

        return resultList

    def range_search2(self, point, radius):
        resultList = []

        for elem in self.storage:
            if point.distance_to(elem.object) <= radius:
                resultList.append(elem.object)

        return resultList

    def nearest_neighbor_depth(self, point, resultdist, num_nodes):
        result = None

        for elem in self.storage:
            distance = point.distance_to(elem.object)
            if distance <= resultdist:
                result = elem.object
                resultdist = distance

        return resultdist, result, num_nodes + 1

    # Performs a split and returns the information about the split
    def split(self, point):
        pointset = self.storage
        pointset.append(RegisterEntry(point, None))

        maxArea = -1

        # 1.- Choose seeds
        for i in range(len(pointset) - 1):
            for j in range(i + 1, len(pointset)):
                point1 = pointset[i].object
                point2 = pointset[j].object

                area = Rect(point1, point1).areaIncrease(Rect(point2, point2))

                if area > maxArea:
                    maxArea = area
                    idx1 = i
                    idx2 = j

        seed1 = pointset.pop(idx1)
        seed2 = pointset.pop(idx2 - 1)

        # 2.- PickNext
        group1 = [seed1]
        group2 = [seed2]

        R1 = Rect(seed1.object, seed1.object)
        R2 = Rect(seed2.object, seed2.object)

        while len(pointset) != 0:
            if len(pointset) + len(group1) == self.m:  # Entries should go in group 1
                group1.extend(pointset)
                for elem in pointset:
                    R1.updateRect(elem.object)
                pointset.clear()
            elif len(pointset) + len(group2) == self.m:  # Entries should go in group 2
                group2.extend(pointset)
                for elem in pointset:
                    R2.updateRect(elem.object)
                pointset.clear()
            else:
                A1 = []
                A2 = []

                # Compute area increase for each entry
                for elem in pointset:
                    A1.append(R1.areaIncrease(Rect(elem.object, elem.object)))
                    A2.append(R2.areaIncrease(Rect(elem.object, elem.object)))

                # Select the bigger difference
                maxDiff = -1
                maxPos = -1

                for i in range(len(A1)):
                    val = abs(A1[i] - A2[i])
                    if val > maxDiff:
                        maxDiff = val
                        maxPos = i

                selectedEntry = pointset.pop(maxPos)
                selectedGroup = 0

                # First criterion is least enlargement
                if A1[maxPos] < A2[maxPos]:
                    selectedGroup = 1
                elif A2[maxPos] < A1[maxPos]:
                    selectedGroup = 2
                else:  # Under same enlargement, the criterion is smaller area
                    if R1.area() < R2.area():
                        selectedGroup = 1
                    elif R1.area() > R2.area():
                        selectedGroup = 2
                    else:  # Under same area, the criterion is fewer entries
                        if len(group1) < len(group2):
                            selectedGroup = 1
                        else:
                            selectedGroup = 2

                if selectedGroup == 1:
                    group1.append(selectedEntry)
                    R1.updateRect(selectedEntry.object)
                else:
                    group2.append(selectedEntry)
                    R2.updateRect(selectedEntry.object)

        return group1, group2, R1, R2

    def nn_rkv(self, point: Point, result_dist: float, pruning_dist: float, num_nodes: int) \
            -> Tuple[float, float, float, int]:
        """
        Calculates the nearest neighbour of a point using the RKV algorithm ("Nearest Neighbor
        Queries", Roussopouls et. al. 1995)
        """
        result = None

        for elem in self.storage:
            distance = point.distance_to(elem.object)
            if distance <= result_dist:
                result = elem.object
                result_dist = distance
                if result_dist < pruning_dist:
                    pruning_dist = result_dist

        return result_dist, pruning_dist, result, num_nodes + 1
