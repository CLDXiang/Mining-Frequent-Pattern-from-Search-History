#!/usr/bin/python3
# -*- coding:utf-8 -*-
#path:/home/hadoop/pj/src/mapper3.py
import sys

for line in sys.stdin:
    line = line.strip()
    pattern, supp = line.split('\t')
    items = pattern.split(' ')

    for item in items:
        print('%s\t%s' % (item, line))  # 输出格式： item \t pattern \t supp
