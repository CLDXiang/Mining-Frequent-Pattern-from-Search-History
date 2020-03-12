# -*- coding:utf-8 -*-
import jieba.analyse
import jieba

def find_pair(combined_parts_path):
    print('正在构建映射表...')
    with open(combined_parts_path, 'r', encoding='utf-8') as f:
        text = f.read()

    lines = [l.strip() for l in text.split('\n') if l.strip()]
    tuples = [(line.split(' ')[0], ' '.join(line.split(' ')[1:])) for line in lines]

    mapper = dict(tuples)    

    while True:
        word = input('请输入想要查找关联模式的关键词：(输入“q”退出)\n')
        if word.lower() == 'q':
            return
        if not word.strip():
            continue

        if word in mapper:
            print(mapper[word])
        else:
            print('没有找到该关键词，一些近似的关键词：')
            keywords = jieba.analyse.extract_tags(word)
            flag = 0
            for kw in keywords:
                if kw in mapper:
                    print('{}:{}'.format(kw, mapper[kw]))
                    flag = 1
            if flag == 0:
                keywords = jieba.cut_for_search(word)
                for kw in keywords:
                    if kw in mapper:
                        print('{}:{}'.format(kw, mapper[kw]))
                        flag = 1
            if flag == 0:
                print('无')
        

if __name__ == '__main__':
    find_pair('./res.txt')