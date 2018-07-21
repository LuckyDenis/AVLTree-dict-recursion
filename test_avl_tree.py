# -*- coding: utf8 -*-

__author__ = 'D. Belavin'


import pytest
from math import ceil
from math import log2
from random import randint

from avl_tree import AVLTree


def create_tree():
    """
    Create and return tree
    """
    return AVLTree()


def test_size():
    """
    Check size tree.

    Check the change in the number of elements in the tree,
    after different operations on it.

    test 1: len new tree == 0
    test 2: len tree after insert 1000 key and del all key == 0
    test 3: len tree after insert 1 and del 1 key == 0
    test 4: len tree after del 50% key
    """
    tree = create_tree()

    # test 1: len new tree == 0
    assert not len(tree)

    # test 2: len tree after insert 1000 key and del all key == 0
    dlist = [randint(1, 100) for i in range(1000)]
    for i in dlist:
        tree[i] = i
    tree.clear_tree()
    assert not len(tree)
    tree.clear_tree()

    # test 3: len tree after insert 1 and del 1 key == 0
    tree[1] = 1
    del tree[1]
    assert not len(tree)
    tree.clear_tree()

    # test 4: len tree after del 50% key
    for i in range(0, 10000):
        tree[i] = i
    for i in range(len(tree) // 2):
        del tree[i]
    tree.clear_tree()


def test_insert_tree():
    """
    Check insert in tree

    Check for duplicate keys.
    Check for an incorrect insert (without a key or value).
    Checking the insertion of a large number of keys.

    test 1: insert tree 1000 key
    test 2: insert tree 10000 payload
    test 3: insert tree 1 key
    test 4: insert tree 0 key
    test 5: insert tree key and not payload
    """
    tree = create_tree()

    # test 1: insert tree 1000 key
    dlist = [randint(1, 100) for i in range(1000)]
    for i in dlist:
        tree[i] = i
    assert len(tree)
    tree.clear_tree()

    # test 2: insert tree 10000 payload
    for i in range(0, 10000):
        tree[i] = i
    assert len(tree) == 10000
    tree.clear_tree()

    # test 3: insert tree 1 key
    tree.clear_tree()
    tree[1] = 1
    assert len(tree) == 1
    tree.clear_tree()

    # test 4: insert tree 0 key
    with pytest.raises(TypeError):
        tree.insert()
    tree.clear_tree()

    # test 5: insert tree key and not payload
    with pytest.raises(TypeError):
        tree.insert(1,)
    tree.clear_tree()


def test_delete():
    """
    Check delete key

    Checking how the tree handles the removal of nodes.

    test 1: del key of tree
    test 2: key not in tree
    test 3: del knot has not children
    test 4: del knot has one child
    test 5: del knot has both children
    test 6: del without key
    test 7: del 50% tree
    """
    tree = create_tree()

    # test 1: del key of tree
    tree[1] = 1
    del tree[1]
    assert not(len(tree))
    tree.clear_tree()

    # test 2: key not in tree
    with pytest.raises(KeyError):
        del tree[3]
    tree.clear_tree()

    # test 3: del knot has not children
    for i in range(10):
        tree[i] = i
    del tree[0]
    temp = []
    for element in tree:
        temp.append(element)
    assert temp == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # test 4: del knot has one child
    del tree[8]
    temp = []
    for element in tree:
        temp.append(element)
    assert temp == [1, 2, 3, 4, 5, 6, 7, 9]

    # test 5: del knot has both children
    del tree[2]
    temp = []
    for element in tree:
        temp.append(element)
    assert temp == [1, 3, 4, 5, 6, 7, 9]
    tree.clear_tree()

    # test 6: del without key
    with pytest.raises(TypeError):
        tree.delete()
    tree.clear_tree()

    # test 7: del 50% tree
    for i in range(0, 10000):
        tree[i] = i
    for i in range(len(tree) // 2):
        del tree[i]
    tree.clear_tree()


def test_del_root():
    """
    Check del root

    We check how the root is removed.

    test 1: root with both children
    test 2: root with left child
    test 3: root with right child
    test 4: root with branch
    """
    tree = create_tree()

    # test 1: del root with both children
    tree[3] = 3
    tree[4] = 4
    tree[2] = 2
    del tree[3]
    assert tree.root.key == 4
    assert tree.root.payload == 4
    assert tree.root.left.key == 2
    assert tree.root.right is None
    tree.clear_tree()

    # test 2: del root with left child
    tree[3] = 3
    tree[2] = 2
    del tree[3]
    assert len(tree) == 1
    assert tree.root.key == 2
    assert tree.root.payload == 2
    assert tree.root.left is None
    assert tree.root.right is None
    tree.clear_tree()

    # test 3: del root with right child
    tree[3] = 3
    tree[4] = 4
    del tree[3]
    assert len(tree) == 1
    assert tree.root.key == 4
    assert tree.root.payload == 4
    assert tree.root.left is None
    assert tree.root.right is None
    tree.clear_tree()

    # test 4: del root with branch
    for i in range(10):
        tree[i] = i
    old_root_key = tree.root.key
    old_root_payload = tree.root.payload
    del tree[old_root_key]
    assert tree.root.key != old_root_key
    assert tree.root.payload != old_root_payload
    assert tree.root.left is not None
    assert tree.root.right is not None
    tree.clear_tree()


def test_get():
    """
    Check get key

    We check how the tree processes requests for get () - errors, value.

    test 1: key in tree
    test 2: key not in tree
    test 3: del key and get key of tree
    test 4: del key, insert key and get key of tree
    """
    tree = create_tree()
    for i in range(10):
        tree[i] = i

    # test 1: key in tree
    assert tree[0] == 0
    assert tree[9] == 9

    # test 2: key not in tree
    assert tree[10] is None

    # test 3: del key and get key of tree
    del tree[0]
    assert tree[0] is None

    # test 4: del key, insert key and get key of tree
    del tree[1]
    tree[1] = 1
    assert tree[1] == 1
    tree.clear_tree()


def test_balance():
    """
    Check height tree

    Check height by 1.04 * log(2, n + 2) with round up.

    test 1: check height tree
    test 2: check height tree after del 50% tree
    """

    tree = create_tree()

    # test 1: check height tree
    for i in range(10000):
        tree[i] = i
    max_height = ceil(1.05 * log2(len(tree) + 2))
    assert tree.root.height <= max_height

    # test 2: check height tree after del 50% tree
    for i in range(len(tree) // 2):
        del tree[i]
    max_height = ceil(1.05 * log2(len(tree) + 2))
    assert tree.root.height <= max_height
