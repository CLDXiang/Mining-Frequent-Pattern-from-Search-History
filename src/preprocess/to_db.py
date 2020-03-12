# -*- coding:utf-8 -*-
from os import listdir, path
import re
from utils import def_log_print


def file_to_db(input_file_path, output_file_path):
    uid2keywords = {}  # 用户ID到当日搜索过的所有关键词的映射
    with open(input_file_path, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:
                break

            line = line.strip()
            uid, keywords, _, _, _ = line.split('\t')
            keywords = keywords[1:-1]  # 去掉中括号

            # 切分关键词：第一种策略：仅通过加号和空白符
            keywords = list(set([kw.strip() for kw in re.split(r'[+\s]', keywords) if kw.strip() != '']))

            if uid not in uid2keywords:
                uid2keywords[uid] = keywords
            else:
                for kw in keywords:
                    if kw not in uid2keywords[uid]:
                        uid2keywords[uid].append(kw)

    # 只有一个关键词的就不用留下了
    transactions = ['\t'+' '.join(t) for t in uid2keywords.values() if len(t) > 1]  # 事务集 加 \t 是因为第一个 Map 输入键为空
    count = len(transactions)
    text = '\n'.join(transactions)

    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(text)

    return count


def to_db_all():
    log_print = def_log_print('to_db')
    data_dir = '../../data/'
    count_total = 0
    files = [file_name for file_name in listdir(path.join(data_dir, 'clean')) if
                  file_name.endswith('.txt')]

    for file in files:
        log_print(f'正在处理 {file}...')
        count = file_to_db(path.join(data_dir, 'clean', file),
                                                    path.join(data_dir, 'DB', file)[
                                                    :-len('.txt')]+'_DB.txt')

        log_print(f'事务条数： {count}')
        count_total += count

    log_print(f'总和： 事务条数： {count_total}')


if __name__ == '__main__':
    to_db_all()
