import configparser


def getPro(file):

    config = configparser.ConfigParser()
    config.read(file)

    return config