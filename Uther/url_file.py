# coding=utf-8
import os


def __url_2_path__(url):
    temp = url
    temp = temp.replace('?', '_')
    temp = temp.replace('.', '_')
    temp = temp.replace(':', '_')
    temp = temp.replace('/', '_')
    temp = ".\\html\\" + temp + ".html"
    return temp


def save_cache(url, text):
    path = __url_2_path__(url)
    save_file(path, text)


def load_cache(url):
    path = __url_2_path__(url)
    return load_file(path)


def exist_cache(url):
    path = __url_2_path__(url)
    return exist_file(path)


def exist_file(file_path):
    return os.path.isfile(file_path)


def save_file(file_path, text):
    file_object = open(file_path, 'w', encoding='utf-8')
    file_object.write(text)
    file_object.close()


def load_file(file_path):
    file_object = open(file_path, 'r', encoding='utf-8')
    text = file_object.read()
    file_object.close()
    return text
