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
    import random

    rng = random.Random()

    tree = RTree(2, 5)
    for _ in range(0, 100):
        tree.insert(Point(rng.random() * 100, rng.random() * 100))
    tree.draw(100, 100)
