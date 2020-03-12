#!/usr/bin/python3
#path:/home/hadoop/pj/src/reducer1.py
import sys

current_word = None  # 为当前单词
current_count = 0  # 当前单词频数
word = None

for line in sys.stdin:
    words = line.strip()  # 去除字符串首尾的空白字符
    word, count = words.split('\t')  # 按照制表符分隔单词和数量

    try:
        count = int(count)  # 将字符串类型的‘1’转换为整型1
    except ValueError:
        continue

    if current_word == word:  # 如果当前的单词等于读入的单词
        current_count += count  # 单词频数加1
    else:
        if current_word:  # 如果当前的单词不为空则打印其单词和频数
            print('%s\t%s' % (current_word, current_count))
        current_count = count  # 否则将读入的单词赋值给当前单词，且更新频数
        current_word = word

if current_word == word:
    print('%s\t%s' % (current_word, current_count))
