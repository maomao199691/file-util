from hdfs import InsecureClient

def getClient():
    client = InsecureClient("http://hadoop10:9870", user='root')
    return client
