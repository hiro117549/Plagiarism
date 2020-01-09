# 単語辞書を作成するためのモジュール
# 原型を持つ単語は原型に変換してから辞書リストに追加
# 辞書はpickleファイル形式で作成されるため、open_pickleモジュールを使って再び辞書型に戻せる。
import os
import nltk
from nltk.corpus import wordnet as wn
import pickle


def make_word_dic(text, file, flag):
    check_word_list = {'NNS', 'VBD', 'VBG', 'VBN', 'JJR', 'JJS', 'RBR', 'RBS'}
    text_info = nltk.word_tokenize(text)  # 単語の分かち書き
    pos = nltk.pos_tag(text_info)  # 単語の情報
    # print(pos)
    # stemmer = nltk.stem.PorterStemmer()  # 原型処理を持つ関数へのアクセス
    # 特定の単語の原型化処理
    for pos_list_num in range(len(pos)):
        if pos[pos_list_num][1] in check_word_list:
            text_info[pos_list_num] = wn.morphy(text_info[pos_list_num])

    # print(text_info)
    with open('./TXT_files/change_root_file/root_' + file + '.pickle', mode='wb') as root_f:
        pickle.dump(text_info, root_f)

    word_dict = []  # テキスト中に出てくる単語のリスト（重複あり）
    if flag:
        for word in text_info:
            if word is not None:
                if word.isalpha() is True and wn.synsets(word):
                    if word.isalpha() is True:
                        word_dict.append(word)
    else:
        for word in text_info:
            if word is not None:
                if word.isalpha() is True:
                    word_dict.append(word)

    # print(word_dict)

    # 辞書ファイルへの書き込み操作
    if os.path.isfile('./dictionary.txt'):
        with open('./dictionary.txt', mode='r') as dic_f:
            exist_word_list = [s.strip() for s in dic_f.readlines()]
        linked_list = word_dict + exist_word_list
        linked_set = set(linked_list)
        text_word_list = sorted(linked_set)
    else:
        text_word_list = sorted(set(word_dict))

    with open('./dictionary.txt', mode='w') as dic_f:
        dic_f.writelines('\n'.join(list(text_word_list)))
    # print(word_dict_sorted)