#!/usr/bin/env python

"""
@author: yangzhitao
@license: Copyright 2017-2020, LineZoneData.
@contact: yangzhitao@linezonedata.com
@software: pycharm
@time: 2019/8/12 4:58
@desc: 
"""
from collections import deque
from enum import Enum


class RBColor(Enum):
    rb_red = 0
    rb_black = 1


class BinNode:
    def __init__(self, data, parent=None, lc=None, rc=None, color=RBColor.rb_red):
        self.data = data
        self.parent = parent
        self.lc = lc
        self.rc = rc
        self.height = 0
        self.npl = 1
        self.color = color

    def size(self):
        """当前节点的后代总数"""
        pass

    def insert_as_lc(self, node):
        self.lc = node
        return self.lc

    def insert_as_rc(self, node):
        self.rc = node
        return self.rc

    @property
    def succ(self):
        """获取节点的直接后继"""
        pass

    # 比较运算
    def __lt__(self, other):
        return self.data < other.data

    def __gt__(self, other):
        return self.data > other.data

    def __le__(self, other):
        return self.data <= other.data

    def __ge__(self, other):
        return self.data >= other.data

    def __eq__(self, other):
        return self.data == other.data


class BinTree:
    def __init__(self):
        self.size = 0
        self.root = None

    @property
    def empty(self):
        return not self.root


def stature(x: BinNode):
    """节点高度。定义空树高度为-1"""
    return x.height if x else -1


def is_root(x: BinNode):
    return not x.parent


def is_l_child(x: BinNode):
    return not is_root(x) and (x is x.parent.lc)


def is_r_child(x: BinNode):
    return not is_root(x) and (x is x.parent.rc)


def has_child(x: BinNode):
    return x.lc or x.rc


def is_leaf(x: BinNode):
    return not has_child(x)


def trav_level(x: BinNode, visit: callable):
    """层次遍历"""
    queue = deque()
    queue.appendleft(x)
    while queue:
        node = queue.pop()
        visit(node)
        if node.lc:
            queue.appendleft(node.lc)
        if node.rc:
            queue.appendleft(node.rc)


def trav_pre(x: BinNode, visit: callable):
    """先序遍历(迭代版)"""
    if not x:
        return
    visit(x)
    trav_pre(x.lc, visit)
    trav_pre(x.rc, visit)


def trav_in(x: BinNode, visit: callable):
    """中序遍历(迭代版)"""
    if not x:
        return
    trav_pre(x.lc, visit)
    visit(x)
    trav_pre(x.rc, visit)


def trav_post(x: BinNode, visit: callable):
    """后序遍历"""
    if not x:
        return
    trav_pre(x.lc, visit)
    trav_pre(x.rc, visit)
    visit(x)
