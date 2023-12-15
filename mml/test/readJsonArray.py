

# 读取大json数组 内存超出问题
import json

import ijson

if __name__ == '__main__':

    file_path = 'E:\\hadoop\\data\\ExcelOut\\info_tag_keyword.json'

    file_dir = 'E:\\hadoop\\data\\ExcelOut\\files'

    data_list = []
    tag = 1
    with open(file_path, 'r', encoding='utf-8') as f:
        objects = ijson.items(f, 'item')
        for obj in objects:
            # 处理每个对象
            # print(obj)
            data_list.append(obj)

            if len(data_list) >= 60000:
                file_out_path = file_dir + '\\info_tag_' + str(tag) + '.json'

                for row in data_list:
                    with open(file_out_path, 'a', encoding='utf-8') as out_f:
                        json.dump(row, out_f, ensure_ascii=False)
                        out_f.write('\n')

                print("生成文件 ===> ", tag)
                data_list = []
                tag = tag + 1

    if len(data_list) > 0:
        file_out_path = file_dir + '\\info_tag_' + str(tag) + '.json'

        for row in data_list:
            with open(file_out_path, 'a', encoding='utf-8') as out_f:
                json.dump(row, out_f, ensure_ascii=False)
                out_f.write('\n')