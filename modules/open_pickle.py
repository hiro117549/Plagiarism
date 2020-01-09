# pickleファイルを開くやつまとめ
import pickle


def open_dic():
    with open('./dictionary.pickle', mode='rb') as f:
        dictionary = pickle.load(f)
    return dictionary


def open_list(file_path):
    with open(file_path, mode='rb') as f:
        text_list = pickle.load(f)
    return text_list
    # print(dictionary)