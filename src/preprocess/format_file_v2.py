# -*- coding:utf-8 -*-
from os import listdir, path
import re
from utils import def_log_print


def Q2B(s):
    """
    全角转半角
    """
    Q = list('ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ０１２３４５６７８９')
    if not any([(c in s) for c in Q]):
        return s
    B = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    Q2Bmap = dict(zip(Q, B))
    res_l = []

    for c in s:
        if c in Q2Bmap:
            res_l.append(Q2Bmap[c])
        else:
            res_l.append(c)

    return ''.join(res_l)

def format_one_file(input_file_path, output_file_path, log_print_fail):
    text = ''
    success_count = 0
    fail_count = 0
    with open(input_file_path, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:
                break

            line = line.strip()
            groups = re.match(r'^([A-Za-z0-9_]+)\s(\[.+\])\s(\d+)\s(\d+)\s([,:+~^|;!$*{}"><\'\`@_A-Za-z0-9\-\[\]\(\)\\./%=?&]+)$', line)
            if not groups:
                log_print_fail(line)
                fail_count += 1
                continue

            g = list(groups.groups())

            # 检查字段数是否正确、各项格式是否正确
            if len(g) != 5 or not g[1].startswith('[') or not g[1].endswith(']') \
                    or not g[2].isnumeric() or not g[3].isnumeric() or not '.' in g[4]:
                log_print_fail(line)
                fail_count += 1
                continue

            # 忽略陋俗
            if '陋俗' in g[1]:
                fail_count += 1
                continue
            g[1] = Q2B(re.sub('\t', ' ', g[1]))  # 去掉关键词里的 tab，把字母和数字全角转半角

            success_count += 1
            text += '\t'.join(g) + '\n'

    with open(output_file_path, 'w') as f:
        f.write(text)

    return success_count, fail_count


def format_all():
    log_print = def_log_print('format_file_v2')
    log_print_fail = def_log_print('format_file_v2_fail')
    data_dir = '../../data/'
    success_count_total, fail_count_total = 0, 0
    temp_files = [file_name for file_name in listdir(path.join(data_dir, 'temp')) if
                  file_name.endswith('.decode.filter.utf8')]

    for temp_file in temp_files:
        log_print(f'正在处理 {temp_file}...')
        success_count, fail_count = format_one_file(path.join(data_dir, 'temp', temp_file),
                                                    path.join(data_dir, 'clean', temp_file)[
                                                    :-len('.decode.filter.utf8')]+'.txt', log_print_fail)

        log_print(f'有效数据条数： {success_count}， 丢弃条数： {fail_count}')
        success_count_total += success_count
        fail_count_total += fail_count

    log_print(f'总和： 有效数据条数： {success_count_total}， 丢弃条数： {fail_count_total}')


if __name__ == '__main__':
    format_all()
