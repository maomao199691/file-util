#!/usr/bin/python
# -*- coding: UTF-8 -*-
import splitutil as spl

import mml.util.getfileutil as tkutil


if __name__ == '__main__':

    file_path = tkutil.get_file_path()

    file_out_dir = tkutil.get_file_dir()

    spl.split_simple_json(in_path=file_path, out_dir=file_out_dir)


    pass