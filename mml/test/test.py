#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import mml.util.getfileutil as tk

if __name__ == '__main__':

    # file_path = 'E:\\hadoop\\data\\ExcelOut\\info_tag\\zh_file\\zh_info_tag1.json'
    #
    # file = os.path.basename(file_path)
    #
    # print(file)

    file_dir = tk.get_file_dir()

    print(file_dir)
