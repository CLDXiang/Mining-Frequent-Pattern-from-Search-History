#!/usr/bin/python3
# -*- coding:utf-8 -*-
# path:/home/hadoop/pj/src/reducer3.py
import sys


current_item = None  # 当前正在处理的 gid
item = None
HP = {}  # 伪最大堆
K = 10  # 输出前 K 个


for line in sys.stdin:
    item, pattern, supp = line.split('\t')
    # print('[DEBUG]', item, pattern, supp)
    if not item:
        continue  # 跳过reducer的输出

    if item != current_item:
        # 此处输出当前最大堆 top K
        if current_item:
            print('\t%s %s' % (current_item, ' '.join([f'[{i[0]}]' for i in sorted(HP.items(), key=lambda x: x[1], reverse=True)[:K]])))

        current_item = item
        HP = {}

    # 更新最大堆
    if pattern in HP:
        HP[pattern] += supp
    else:
        HP[pattern] = supp

if item == current_item:
    # 此处输出当前最大堆 top K
    print('\t%s %s' % (current_item, ' '.join([f'[{i[0]}]' for i in sorted(HP.items(), key=lambda x: x[1], reverse=True)[:K]])))

