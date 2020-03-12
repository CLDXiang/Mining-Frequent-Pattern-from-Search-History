# -*- coding:utf-8 -*-
from os import listdir, path
import re
from utils import def_log_print


def format_one_file(input_file_path, output_file_path):
    text = ''
    success_count = 0
    fail_count = 0
    with open(input_file_path, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:
                break

            line = line.strip()
            line = [i.strip() for i in re.split(r'\s', line) if i]

            # 检查字段数是否正确、各项格式是否正确
            if len(line) != 5 or not line[0].isnumeric() or not line[1].startswith('[') or not line[1].endswith(']') \
                    or not line[2].isnumeric() or not line[3].isnumeric() or not '.' in line[4]:
                fail_count += 1
                continue

            success_count += 1
            text += '\t'.join(line) + '\n'

    with open(output_file_path, 'w') as f:
        f.write(text)

    return success_count, fail_count


def format_all():
    log_print = def_log_print('format_file')
    data_dir = '../../data/'
    success_count_total, fail_count_total = 0, 0
    temp_files = [file_name for file_name in listdir(path.join(data_dir, 'temp')) if
                  file_name.endswith('.decode.filter.utf8')]

    for temp_file in temp_files:
        log_print(f'正在处理 {temp_file}...')
        success_count, fail_count = format_one_file(path.join(data_dir, 'temp', temp_file),
                                                    path.join(data_dir, 'clean', temp_file)[
                                                    :-len('.decode.filter.utf8')])

        log_print(f'有效数据条数： {success_count}， 丢弃条数： {fail_count}')
        success_count_total += success_count
        fail_count_total += fail_count

    log_print(f'总和： 有效数据条数： {success_count_total}， 丢弃条数： {fail_count_total}')


if __name__ == '__main__':
    format_all()
