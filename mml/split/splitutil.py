# 切分不同类型文件方法 单个文件切分
import json
import os
import ijson
import mml.util.ProIniUtil as pro

pro = pro.getPro('pro.ini')
split_count = int(pro.get('split', 'split_count'))

def split_csv(in_path, out_dir):
    file_name = os.path.basename(in_path)

    file_start_name = file_name.split('.')[0]

    data_list = []


    pass


def split_excel():


    pass


# 切一行一行的json文件
def split_simple_json(in_path, out_dir):

    file_name= os.path.basename(in_path)

    file_start_name = file_name.split('.')[0]

    data_list = []

    tag = 1
    with open(in_path, 'r', encoding='utf-8') as f:
        for line in f:
            data_list.append(line)

            if len(data_list) >= split_count:
                file_out_path = out_dir + '/' + file_start_name + '_' + str(tag) + '.json'

                for row in data_list:
                    with open(file_out_path, 'a', encoding='utf-8') as out_f:
                        json.dump(row, out_f, ensure_ascii=False)
                        out_f.write('\n')

                print("正在生成第", tag, '个文件   ===> ', file_out_path)
                data_list = []
                tag += 1

    if len(data_list) > 0:
        file_out_path = out_dir + '/' + file_start_name + '_' + str(tag) + '.json'

        for row in data_list:
            with open(file_out_path, 'a', encoding='utf-8') as out:
                json.dump(row, out, ensure_ascii=False)

    print("json文件分割完成")


# 单行json数组 -> dataGrip 生成json文件
def split_array_json(in_path, out_dir):
    file_name = os.path.basename(in_path)

    file_start_name = file_name.split('.')[0]

    data_list = []
    tag = 1
    with open(in_path, 'r', encoding='utf-8') as f:
        objects = ijson.items(f, 'item')
        for obj in objects:
            # 处理每个对象
            data_list.append(obj)

            if len(data_list) >= split_count:

                file_out_path = out_dir + '/' + file_start_name + '_' + str(tag) + '.json'
                for row in data_list:
                    with open(file_out_path, 'a', encoding='utf-8') as out_f:
                        json.dump(row, out_f, ensure_ascii=False)
                        out_f.write('\n')

                print("正在生成第", tag, '个文件   ===> ', file_out_path)
                data_list = []
                tag = tag + 1

    if len(data_list) > 0:

        file_out_path = out_dir + '/' + file_start_name + '_' + str(tag) + '.json'
        for row in data_list:
            with open(file_out_path, 'a', encoding='utf-8') as out_f:
                json.dump(row, out_f, ensure_ascii=False)
                out_f.write('\n')

        print("json文件分割完成")