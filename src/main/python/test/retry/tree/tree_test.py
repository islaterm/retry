"""
"ReTry" (c) by Ignacio Slater M.
"ReTry" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <https://creativecommons.org/licenses/by/4.0/>.
"""
import random
import sys
import unittest

import pytest
from retry.geometry import Point
from retry.tree.rtree import RTree


@pytest.fixture
def eps() -> float:
    return 1e-10


@pytest.fixture
def num_points() -> int:
    return 100


# region : RANDOM NUMBER GENERATION
def rand_coord(rng: random.Random) -> float:
    return rng.random() * 100


@pytest.fixture()
def seed() -> int:
    return random.randint(0, sys.maxsize)


@pytest.fixture
def rng(seed: int) -> random.Random:
    # return random.Random(1824491819265783747)
    return random.Random(seed)


@pytest.fixture
def rand_point(rng: random.Random) -> Point:
    return Point(rand_coord(rng), rand_coord(rng))


# endregion

# region : R-TREES
@pytest.fixture
def tree() -> RTree:
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
    return tree


@pytest.fixture()
def rand_tree(num_points: int, rng: random.Random) -> RTree:
    tree = RTree(2, 5)
    for _ in range(0, num_points):
        tree.insert(Point(rand_coord(rng), rand_coord(rng)))
    return tree


# endregion

def test_nearest_neighbour(tree: RTree) -> None:
    assert (2.23606797749979, Point(8, 5), 4) == tree.nearest_neighbor_depth(Point(9, 3))


def test_rkv(tree: RTree) -> None:
    result_dist, pruning_dist, nearest_point, num_nodes = tree.nnRKV(Point(9, 3))
    assert result_dist == pruning_dist
    assert (2.23606797749979, Point(8, 5)) == (result_dist, nearest_point)


@pytest.mark.repeat(100)
def test_nn_consistency(rand_tree: RTree, rand_point: Point, eps: float, seed: int) -> None:
    rkv_dist, _, rkv_nn, rkv_num_nodes = rand_tree.nnRKV(rand_point)
    naive_dist, naive_nn, naive_num_nodes = rand_tree.nearest_neighbor_depth(rand_point)
    if rkv_nn is not None and naive_nn is not None:
        assert abs(rkv_dist - naive_dist) < eps, f"Test failed with random seed: {seed}"
        assert rkv_nn == naive_nn, f"Test failed with random seed: {seed}"
        assert rkv_num_nodes <= naive_num_nodes, f"Test failed with random seed: {seed}"


if __name__ == '__main__':
    unittest.main()
