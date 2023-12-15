#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pyspark.sql import SparkSession
import mml.util.HdfsClientUtil as hdfs

client = hdfs.getClient()

# 将表下的经过合并后的原文件移动到临时目录下存储
# table_location_path: 需要合并表的路径    table_tmp_path: 需要合并表的数据临时保存目录
def move_file_tmp(dir,path1):

    table_tmp_path = '/tmp/hive-tmp'
    if "/" in dir:
        split_path = dir.split("/")
        table_part = "/".join(split_path[2:])

        hdfs_tmp_path = table_tmp_path + '/' + table_part

        exists = client.content(hdfs_tmp_path, strict=False) is not None

        if not exists:
            client.makedirs(hdfs_tmp_path)

        file_name = path1.split("/")[-1]
        client.rename(path1, hdfs_tmp_path + "/" + file_name)


def merge_files(session, table_path, dir, path1, path2):


    hdfs_path = 'hdfs://hadoop10:8020'
    hdfs_file1 = hdfs_path + path1
    hdfs_file2 = hdfs_path + path2

    hdfs_tmp_path = table_path + "/merge_tmp"
    save_tmp_path = hdfs_path + table_path + "/merge_tmp"


    df1 = session.read.parquet(hdfs_file1)
    df2 = session.read.parquet(hdfs_file2)

    merge_df = df1.union(df2)

    # 写入合并文件到临时目录
    merge_df.coalesce(1).write.parquet(save_tmp_path)


    # 将合并后的文件移动到原来的表分区中
    tmp_files = client.list(hdfs_tmp_path)
    for tmp_file in tmp_files:
        if 'parquet' in tmp_file:
            ori_path = hdfs_tmp_path + "/" + tmp_file
            move_path = dir + "/" + tmp_file

            client.rename(ori_path, move_path)

            client.delete(hdfs_tmp_path, recursive=True)


# 合并hive单分区下的 snappy.parquet 文件
if __name__ == '__main__':

    session = SparkSession.builder.appName("test").getOrCreate()

    table_location_path = '/gkza-db/info_collect_tmp'

    # 获取目录下所有文件
    def list_files(path):
        files = client.list(path)

        for file in files:
            file_path = path + '/' + file

            exists = client.content(file_path, strict=False) is not None
            if exists:

                file_type = client.status(file_path)['type']
                if file_type == 'DIRECTORY':
                    list_files(file_path)
                else:

                    # 同级目录下合并
                    print("上级路径 => ", path)
                    print("文件路径 => ", file_path)


                    file_size = client.status(file_path)['length']

                    # 遍历了自身的其他文件
                    other_files = client.list(path)
                    for other_file in other_files:
                        if  file != other_file:

                            other_file_path = path + '/' + other_file
                            other_file_type = client.status(other_file_path)['type']

                            if other_file_type != 'DIRECTORY':
                                other_file_size = client.status(other_file_path)['length']

                                # 合并条件： 获取第一个文件大小，如果和第二个文件大小相加小于128M就合并，大于就和第三个文件相加依次类推
                                count_size = file_size + other_file_size
                                if count_size < 134217728:

                                    # 合并文件并移动到表分区目录下
                                    merge_files(session, table_location_path, path, file_path, other_file_path)

                                    # 将合并的文件移动到临时目录下
                                    move_file_tmp(path, file_path)
                                    move_file_tmp(path, other_file_path)
                                    break


    list_files(table_location_path)

    print("文件合并完毕!!!")

    session.stop()