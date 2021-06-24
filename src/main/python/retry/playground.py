"""
"ReTry" (c) by Ignacio Slater M.
"ReTry" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <https://creativecommons.org/licenses/by/4.0/>.
"""
from retry.geometry import Point
from retry.tree.rtree import RTree

if __name__ == '__main__':
    tree = RTree(2, 5)

    tree.insert(Point(8, 10))
    tree.insert(Point(4, 10))
    tree.insert(Point(6, 4))
    tree.insert(Point(1, 10))
    tree.insert(Point(6, 5))
    tree.insert(Point(5, 4))
    tree.insert(Point(7, 8))
    tree.insert(Point(3, 2))
    tree.insert(Point(10, 7))
    tree.insert(Point(2, 3))
    tree.insert(Point(8, 5))
    tree.insert(Point(4, 5))

    tree.draw(10, 10)
