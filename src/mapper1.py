#!/usr/bin/python3
#path:/home/hadoop/pj/src/mapper1.py
import sys

for line in sys.stdin:
    line = line.strip()
    items = line.split()  # 按空格将句子分割成单个单词
    for item in items:
        print('%s\t%s' % (item, 1))