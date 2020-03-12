#!/usr/bin/python3
# -*- coding:utf-8 -*-
# path:/home/hadoop/pj/src/reducer2.py
import sys


class Node(object):
    def __init__(self, item='', parent=None):
        self.item = item
        self.count = 1
        self.parent = parent
        self.children = []

    def add_count(self):
        self.count += 1

    def set_count(self, c):
        self.count = c

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        return child

    def find_child(self, item):
        for c in self.children:
            if c.item == item:
                return c
        return None

    def get_self(self):
        return self

    def scan(self, HP, ancestors):
        # 对当前节点，将其和所有祖先的对加上当前的 supp
        for ancestor in ancestors:
            pair = ' '.join([ancestor, self.item])
            if pair in HP:
                HP[pair] += self.count
            else:
                HP[pair] = self.count

        for c in self.children:
            if self.item:
                c.scan(HP, ancestors[:]+[self.item])
            else:
                c.scan(HP, ancestors[:])

    def __str__(self):
        return f'{self.item}:{self.count} at {id(self)}'


root = Node()
current_gid = 1  # 当前正在处理的 gid
gid = None
HP = {}  # 伪最大堆
K = 50

for line in sys.stdin:
    words = line.strip()  # 去除字符串首尾的空白字符
    gid, items = words.split('\t')
    if ' ' in gid:
        continue  # 跳过reducer的输出
    try:
        int(gid)
    except ValueError:
        continue


    items = items.split(' ')

    if len(items) == 0:
        continue

    if gid != current_gid:
        # 此处通过当前的树弄出最大堆
        root.scan(HP, [])

        root = Node()
        current_gid = gid

        # 此处输出当前最大堆 top K
        for k, v in sorted(HP.items(), key=lambda x: x[1], reverse=True)[:K]:
            print('%s\t%s' % (k, v))  # 输出 模式串\t支持度

        HP = {}

    # 此处建树
    p = root.get_self()
    for item in items:
        child = p.find_child(item)
        if child:
            child.add_count()
            p = child.get_self()
        else:
            p = p.add_child(Node(item))


if gid == current_gid:
    # 此处输出当前最大堆 top K
    for k, v in sorted(HP.items(), key=lambda x: x[1], reverse=True)[:K]:
        print('%s\t%s' % (k, v))  # 输出 模式串\t支持度
