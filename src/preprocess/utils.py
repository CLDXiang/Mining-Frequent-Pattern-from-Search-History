# -*- coding:utf-8 -*-
import time


def def_log_print(name):
    with open(f'../../log/{name}.txt', 'a', encoding='utf-8') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'\n')

    def log_print(content):
        print(content)
        with open(f'../../log/{name}.txt', 'a', encoding='utf-8') as f:
            f.write(content+'\n')
    return log_print


def log(content, name):
    with open(f'../../log/{name}.txt', 'a') as f:
        f.write(content+'\n')
