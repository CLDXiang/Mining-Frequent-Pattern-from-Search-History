#!/usr/bin/python3
# -*- coding:utf-8 -*-
#path:/home/hadoop/pj/src/mapper2.py
import sys

G_list = {} # TODO: 将输出的 G_list 粘贴在此

for line in sys.stdin:
    line = line.strip()
    items = line.split()  # 按空格将句子分割成单个单词

    used_gid = []

    for i in range(len(items)-1, -1, -1):
        gid = G_list[items[i]]
        if gid in used_gid:
            continue
        else:
            used_gid.append(gid)
            print('%s\t%s' % (gid, ' '.join(items[:i+1])))
