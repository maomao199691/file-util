#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import re

import mml.util.getfileutil as tkutil



def get_file_name(file_path):
    file_names = file_path.split("/")
    filename_all = file_names[-1]

    filename = filename_all.split(".")[0]
    return filename

# 按照正则切分文件, 比如一个excel按照 title 列切分为中文和英文  '[\\p{IsHan}]'
if __name__ == '__main__':

    file_path = tkutil.get_file_path()

    out_dir = tkutil.get_file_dir()

    file_name = get_file_name(file_path)

    pattern = re.compile(r'[\u4e00-\u9fff]+')

    data_zh = []
    data_en = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
             data = json.loads(line)
             split_key = data['标题']

             match = pattern.search(split_key)

             if match:
                 data_zh.append(data)
             else:
                 data_en.append(data)

    zh_file_out_path = out_dir + "/" + file_name + "_zh.json"
    en_file_out_path = out_dir + "/" + file_name + "_en.json"

    with open(zh_file_out_path, 'w', encoding='utf-8') as f:
        for line in data_zh:
            json.dump(line, f, ensure_ascii=False)
            f.write('\n')

        print("满足正则的文件已生成!!!")

    with open(en_file_out_path, 'w', encoding='utf-8') as f:
        for line in data_en:
            json.dump(line, f, ensure_ascii=False)
            f.write('\n')

        print("不满足正则的文件已生成!!!")

    print("文件切割完毕!!!")