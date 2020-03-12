# -*- coding:utf-8 -*-
from os import listdir, path

def combine_parts(input_dir_path,output_file_path):
    parts = [file_name for file_name in listdir(input_dir_path) if
                 file_name.startswith('part-')]
    with open(output_file_path, 'w', encoding='utf-8') as f_o:
        f_o.write('') # 清空文件

    text = []
    
    for part in parts:
        print('正在读取 {}...'.format(part))
        with open(path.join(input_dir_path, part), 'r', encoding='utf-8') as f_i:
            text.append(f_i.read().rstrip())

    with open(output_file_path, 'a', encoding='utf-8') as f_o:
        f_o.write('\n'.join(text))


if __name__ == '__main__':
    combine_parts('../../final_test/final_res', '../../final_test/res.txt')
