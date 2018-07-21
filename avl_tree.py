# -*- coding: utf8 -*-

__author__ = 'D. Belavin'


class NodeTree:
    __slots__ = ['key', 'payload', 'parent', 'left', 'right', 'height']

    def __init__(self, key, payload, parent=None, left=None, right=None):
        self.key = key
        self.payload = payload
        self.parent = parent
        self.left = left
        self.right = right
        self.height = 1

    def has_left_child(self):
        return self.left

    def has_right_child(self):
        return self.right

    def is_left_knot(self):
        return self.parent and self.parent.left == self

    def is_right_knot(self):
        return self.parent and self.parent.right == self

    def is_root(self):
        return not self.parent

    def has_leaf(self):
        return not(self.left or self.right)

    def has_any_children(self):
        return self.left or self.right

    def has_both_children(self):
        return self.left and self.right

    def replace_node_date(self, key, payload, left, right):
        # swap root and his child (left or right)
        self.key = key
        self.payload = payload
        self.left = left
        self.right = right
        if self.has_left_child():
            self.left.parent = self
        if self.has_right_child():
            self.right.parent = self

    def find_min(self):
        curr = self
        while curr.has_left_child():
            curr = curr.left
        return curr

    def find_successor(self):
        succ = None
        # has right child
        if self.has_right_child():
            succ = self.right.find_min()
        else:
            if self.parent:
                # self.parent.left == self
                if self.is_left_knot():
                    succ = self.parent
                else:
                    self.parent.right = None  # say that there is no right child
                    succ = self.parent.find_successor()  # from the left of the parent
                    self.parent.right = self  # return the right child to the place
        return succ

    def splice_out(self):
        # cut off node
        if self.has_leaf():
            # self.parent.left == self
            if self.is_left_knot():
                self.parent.left = None
            # self.parent.right == self
            else:
                self.parent.right = None
        # self has left or right child
        elif self.has_any_children():
            # has left child
            if self.has_left_child():
                # self.parent.left == self
                if self.is_left_knot():
                    self.parent.left = self.left
                # self.parent.right == self
                else:
                    self.parent.right = self.left
                # give away parent
                self.left.parent = self.parent
            # has right child
            else:
                # self.parent.left == self
                if self.is_left_knot():
                    self.parent.left = self.right
                # self.parent.right == self
                else:
                    self.parent.right = self.right
                # give away parent
                self.right.parent = self.parent

    def __iter__(self):
        if self:
            if self.has_left_child():
                for element in self.left:
                    yield element
            yield self.key
            if self.has_right_child():
                for element in self.right:
                    yield element


class AVLTree:

    def __init__(self):
        self.root = None
        self.size = 0

    def _height(self, node):
        if node:
            return node.height
        return 0

    def _get_balance(self, node):
        if node:
            return self._height(node.left) - self._height(node.right)
        return 0

    def _height_up(self, node):
        # exhibit the height
        return 1 + max(self._height(node.left), self._height(node.right))

    def _left_rotate(self, rot_node):
        # rot_node.right = rot_node.right.left
        new_node = rot_node.right
        rot_node.right = new_node.left
        # give away left child
        if new_node.has_left_child():
            new_node.left.parent = rot_node
        # give away parent
        new_node.parent = rot_node.parent
        # rot_node == self.root
        if rot_node.is_root():
            self.root = new_node
            new_node.parent = None
        else:
            # rot_node.parent.left == rot_node
            if rot_node.is_left_knot():
                rot_node.parent.left = new_node
            # rot_node.parent.right == rot_node
            else:
                rot_node.parent.right = new_node
        # rot_node is left child new_node
        new_node.left = rot_node
        rot_node.parent = new_node
        # exhibit the height
        rot_node.height = self._height_up(rot_node)
        new_node.height = self._height_up(new_node)

    def _right_rotate(self, rot_node):
        # rot_node.left = rot_node.left.right
        new_node = rot_node.left
        rot_node.left = new_node.right
        # give away right child
        if new_node.has_right_child():
            new_node.right.parent = rot_node
        # give away parent
        new_node.parent = rot_node.parent
        # rot_node == self.root
        if rot_node.is_root():
            self.root = new_node
            new_node.parent = None
        else:
            # rot_node.parent.left == rot_node
            if rot_node.is_left_knot():
                rot_node.parent.left = new_node
            # rot_node.parent.right == rot_node
            else:
                rot_node.parent.right = new_node
        # rot_node is right child new_node
        new_node.right = rot_node
        rot_node.parent = new_node
        # exhibit the height
        rot_node.height = self._height_up(rot_node)
        new_node.height = self._height_up(new_node)

    def _fix_balance(self, node):
        node.height = self._height_up(node)
        balance = self._get_balance(node)
        if balance > 1:
            # big left rotate
            if self._get_balance(node.left) < 0:
                self._left_rotate(node.left)
                self._right_rotate(node)
            # small right rotate
            else:
                self._right_rotate(node)
        elif balance < -1:
            # big right rotate
            if self._get_balance(node.right) > 0:
                self._right_rotate(node.right)
                self._left_rotate(node)
            # small left rotate
            else:
                self._left_rotate(node)

    def _insert(self, key, payload, curr_node):
        # Important place. Responsible for inserting duplicate keys.
        # If you remove these conditions, you can set duplicate keys.
        # If we leave, we get the structure of a dict (map).
        # If we leave this condition, and remove the payload,
        # then we get the basis for the "set" structure.
        if key == curr_node.key:
            curr_node.payload = payload
        else:
            # go to the left
            if key < curr_node.key:
                if curr_node.has_left_child():
                    self._insert(key, payload, curr_node.left)
                else:  # curr_node.left == None
                    curr_node.left = NodeTree(key, payload, parent=curr_node)
                    self.size += 1
            # go to the right
            else:
                if curr_node.has_right_child():
                    self._insert(key, payload, curr_node.right)
                else:  # curr_node.right == None
                    curr_node.right = NodeTree(key, payload, parent=curr_node)
                    self.size += 1
            self._fix_balance(curr_node)

    def insert(self, key, payload):
        if self.root:
            self._insert(key, payload, self.root)
        else:
            self.root = NodeTree(key, payload)
            self.size += 1

    def _get(self, key, curr_node):
        # find not key, stop recursion
        if not curr_node:
            return None
        # find key, stop recursion
        elif key == curr_node.key:
            return curr_node
        # go to the left
        elif key < curr_node.key:
            return self._get(key, curr_node.left)
        # go to the right
        else:
            return self._get(key, curr_node.right)

    def get(self, key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.payload
            else:
                return None  # can be replaced by an "raise KeyError"
        else:
            return None  # can be replaced by an "raise KeyError"

    def _delete(self, node):
        if node.has_leaf():  # node not has children
            # node.parent.left == node
            if node.is_left_knot():
                node.parent.left = None
            # node.parent.right == node
            else:
                node.parent.right = None
            self._fix_balance(node.parent)
        elif node.has_both_children():  # node has two children
            succ = node.find_successor()
            succ.splice_out()
            node.key = succ.key
            node.payload = succ.payload
            self._fix_balance(succ.parent)
        else:  # node has any child
            if node.has_any_children():
                # has left child
                if node.has_left_child():
                    # node.parent.left == node
                    if node.is_left_knot():
                        node.parent.left = node.left
                        node.left.parent = node.parent
                        self._fix_balance(node.parent)
                    # node.parent.right == node
                    elif node.is_right_knot():
                        node.parent.right = node.left
                        node.left.parent = node.parent
                        self._fix_balance(node.parent)
                    else:
                        # node has not parent, means node == self.root
                        # but node has left child
                        node.replace_node_date(node.left.key,
                                               node.left.payload,
                                               node.left.left,
                                               node.left.right)
                        self._fix_balance(node)
                # has right child
                else:
                    # node.parent.left == node
                    if node.is_left_knot():
                        node.parent.left = node.right
                        node.right.parent = node.parent
                        self._fix_balance(node.parent)
                    # node.parent.right == node
                    elif node.is_right_knot():
                        node.parent.right = node.right
                        node.right.parent = node.parent
                        self._fix_balance(node.parent)
                    else:
                        # node has not parent, means node == self.root
                        # but node has right child
                        node.replace_node_date(node.right.key,
                                               node.right.payload,
                                               node.right.left,
                                               node.right.right)
                        self._fix_balance(node)

    def delete(self, key):
        if self.size > 1:
            remove_node = self._get(key, self.root)
            if remove_node:
                self._delete(remove_node)
                self.size -= 1
            else:
                raise KeyError('key not in tree.')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size -= 1
        else:
            raise KeyError('key not in tree.')

    def __len__(self):
        return self.size

    def __setitem__(self, key, payload):
        self.insert(key, payload)

    def __delitem__(self, key):
        self.delete(key)

    def __getitem__(self, key):
        return self.get(key)

    def __contains__(self, key):
        if self._get(key, self.root):
            return True
        else:
            return False

    def __iter__(self):
        return self.root.__iter__()

    def clear_tree(self):
        self.root = None
        self.size = 0
