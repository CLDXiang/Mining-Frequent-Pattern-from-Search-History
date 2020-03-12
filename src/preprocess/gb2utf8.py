# -*- coding:utf-8 -*-
from os import listdir, path
from utils import def_log_print


def gb2utf8_all():
    log_print = def_log_print('gb2utf8')
    data_dir = '../../data/'
    raw_files = [file_name for file_name in listdir(path.join(data_dir, 'raw/SogouQ')) if
                 file_name.endswith('.decode.filter')]

    for raw_file in raw_files:
        log_print(f'正在处理 {raw_file}...')

        text = ''
        fail_count = 0
        cnt = 0

        with open(path.join(data_dir, 'raw/SogouQ', raw_file), 'r', encoding='gb18030') as f:
            while True:
                try:
                    line = f.readline()
                except UnicodeDecodeError:
                    fail_count += 1
                    continue
                if not line:
                    break
                text += line
        if fail_count:
            log_print(f'无法识别的行数：{fail_count}')
        with open(path.join(data_dir, 'temp', raw_file) + '.utf8', 'w', encoding='utf-8') as f:
            f.write(text)


if __name__ == '__main__':
    gb2utf8_all()
