# -*- coding:utf-8 -*-

def sort_file(input_file_path, F_list_path, G_list_path, I):
    with open(input_file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    lines = [l.split('\t') for l in text.split('\n') if l.strip() != '']
    lines.sort(key=lambda x: int(x[1]), reverse=True)
    items_count = len(lines)
    print(f'项目总数：{items_count}')

    F, G = [], []
    for i in range(items_count):
        l = lines[i]
        F.append('\t'.join(l))
        G.append('\t'.join([l[0], str(int(i / I) + 1)]))

    with open(F_list_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(F))
    with open(G_list_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(G))


def file2JSON(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    lines = [l.split('\t') for l in text.split('\n') if l.strip() != '']
    res = dict(lines)

    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(str(res))


if __name__ == '__main__':
    sort_file('../final_test/final_res1/part-00000', '../data/result/F_list.txt', '../data/result/G_list.txt', 100)
    file2JSON('../data/result/G_list.txt', '../data/result/G_list.json')
    # sort_file('../temp/part-00000', '../data/result/F_list_10.txt', '../data/result/G_list_10.txt', 10)
    # file2JSON('../data/result/G_list_10.txt', '../data/result/G_list_10.json')
    # sort_file('../temp/part-00000', '../data/result/F_list_100.txt', '../data/result/G_list_100.txt', 100)
    # file2JSON('../data/result/G_list_100.txt', '../data/result/G_list_100.json')
    # sort_file('../temp/part-00000', '../data/result/F_list_1000.txt', '../data/result/G_list_1000.txt', 1000)
    # file2JSON('../data/result/G_list_1000.txt', '../data/result/G_list_1000.json')
    # sort_file('../temp/part-00000', '../data/result/F_list_10000.txt', '../data/result/G_list_10000.txt', 10000)
    # file2JSON('../data/result/G_list_10000.txt', '../data/result/G_list_10000.json')
