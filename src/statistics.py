# -*- coding:utf-8 -*-
from os import listdir, path
import re

def statistics():
    data_dir = '../data/'
    count = 0
    res_dict = {}
    files = [file_name for file_name in listdir(path.join(data_dir, 'DB')) if
                  file_name.endswith('.txt')]

    for file in files:
        print(f'正在处理 {file}...')

        with open(path.join(data_dir, 'DB', file), 'r', encoding='utf-8') as f:
            text = f.read()

        words = [w.strip() for w in re.split(r'\s', text) if w.strip() != '']

        for w in words:
            if w not in res_dict:
                res_dict[w] = 1
            else:
                res_dict[w] += 1

    print('排序中...')
    res = sorted(res_dict.items(), key=lambda x: x[1], reverse=True)
    print('排序完成')

    res_text = ''
    for t in res:
        res_text += f'{t[0]}\t{t[1]}\n'

    with open(path.join(data_dir, 'stat', 'statistics.txt'), 'w', encoding='utf-8') as f:
        f.write(res_text)

    print(f'总和： 项目数： {len(res)}')


if __name__ == '__main__':
    statistics()
