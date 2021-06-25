"""
"ReTry" (c) by Ignacio Slater M.
"ReTry" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <https://creativecommons.org/licenses/by/4.0/>.
"""
from typing import List

from retry.geometry import Point, Rect
from retry.tree.commons import Node, RegisterEntry
from retry.tree.leaf import NodeLeaf


def _mindist(entry: RegisterEntry, point: Point) -> float:
    return entry.object.mindist(point)


class NodeDirectory(Node):
    storage: List[RegisterEntry]

    def __init__(self, m, M):
        self.m = m
        self.M = M
        self.storage = []

    def __str__(self):
        auxStr = "| "
        for elem in self.storage:
            auxStr = auxStr + f"{elem.object.__str__()} | "

        return auxStr

    def draw(self, ax):
        print(len(self.storage))
        for elem in self.storage:
            elem.object.draw(ax)
            elem.pointer.draw(ax)

    def range_search(self, rect):
        L = []

        for elem in self.storage:
            if rect.has_overlap(elem.object):
                L = L + elem.pointer.range_search(rect)

        return L

    def range_search2(self, point, radius):
        L = []

        for elem in self.storage:
            if elem.object.mindist(point) <= radius:
                L = L + elem.pointer.range_search2(point, radius)

        return L

    def nearest_neighbor_depth(self, point, resultdist, num_nodes):
        result = None

        for elem in self.storage:
            if elem.object.mindist(point) <= resultdist:
                (resultdist, result, num_nodes) = elem.pointer.nearest_neighbor_depth(point,
                                                                                      resultdist,
                                                                                      num_nodes)

        return resultdist, result, num_nodes + 1

    def nn_rkv(self, point, resultdist, pruningdist, num_nodes):
        result = None
        objects: List[RegisterEntry] = []
        elem: RegisterEntry
        for elem in self.storage:
            objects.append(elem.object)
            minmax_dist = elem.object.minmaxdist(point)
            if minmax_dist <= pruningdist:
                pruningdist = minmax_dist
        objects = sorted(self.storage, key=lambda entry: _mindist(entry, point))
        for elem in objects:
            if _mindist(elem, point) <= pruningdist:
                resultdist, pruningdist, result, num_nodes = elem.pointer.nn_rkv(
                    point, resultdist, pruningdist, num_nodes)
                pass
        return resultdist, pruningdist, result, num_nodes + 1

    def insertPoint(self, point):
        minEnl = 100000000
        minPos = -1

        # Select the rectangle with the least enlargement
        for i in range(len(self.storage)):
            val = self.storage[i].object.areaIncrease(Rect(point, point))
            if val < minEnl:
                minEnl = val
                minPos = i

        result = self.storage[minPos].pointer.insertPoint(point)

        if result[0] == False:
            self.storage[minPos].object.updateRect(point)
            return (False, None)
        else:
            (flag, L, LL, rect1, rect2) = result

            # First group overwrite the content of children where the insertion happened
            self.storage[minPos].pointer.storage = L
            self.storage[minPos].object = rect1

            if isinstance(self.storage[minPos].pointer, NodeLeaf):
                newNode = NodeLeaf(self.m, self.M)
            else:
                newNode = NodeDirectory(self.m, self.M)

            newNode.storage = LL
            # There is capacity to store the new node?
            if len(self.storage) < self.M:
                self.storage.append(RegisterEntry(rect2, newNode))
                return (False, None)

            L, LL, R1, R2 = self.split(RegisterEntry(rect2, newNode))

            return (True, L, LL, R1, R2)

    def split(self, re):
        rectset = self.storage
        rectset.append(re)

        maxArea = -1

        # Choose seeds
        for i in range(len(rectset) - 1):
            for j in range(i + 1, len(rectset)):
                rect1 = rectset[i].object
                rect2 = rectset[j].object

                area = rect1.areaIncrease(rect2) - rect2.area()

                if area > maxArea:
                    maxArea = area
                    idx1 = i
                    idx2 = j

        seed1 = rectset.pop(idx1)
        seed2 = rectset.pop(idx2 - 1)

        group1 = [seed1]
        group2 = [seed2]

        R1 = Rect(seed1.object.topLeft, seed1.object.bottomRight)
        R2 = Rect(seed2.object.topLeft, seed2.object.bottomRight)

        while len(rectset) != 0:
            if len(rectset) + len(group1) == self.m:
                group1.extend(rectset)
                for elem in rectset:
                    R1.updateRect(elem.object)
                rectset.clear()
            elif len(rectset) + len(group2) == self.m:
                group2.extend(rectset)
                for elem in rectset:
                    R2.updateRect(elem.object)
                rectset.clear()
            else:
                A1 = []
                A2 = []

                for elem in rectset:
                    A1.append(R1.areaIncrease(elem.object))
                    A2.append(R2.areaIncrease(elem.object))

                maxDiff = -1
                maxPos = -1

                for i in range(len(A1)):
                    val = abs(A1[i] - A2[i])
                    if val > maxDiff:
                        maxDiff = val
                        maxPos = i

                selectedEntry = rectset.pop(maxPos)
                selectedGroup = 0

                if A1[maxPos] < A2[maxPos]:
                    selectedGroup = 1
                elif A2[maxPos] < A1[maxPos]:
                    selectedGroup = 2
                else:
                    if R1.area() < R2.area():
                        selectedGroup = 1
                    elif R1.area() > R2.area():
                        selectedGroup = 2
                    else:
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
