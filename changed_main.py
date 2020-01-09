import sys
import subprocess
import glob
import xml.etree.ElementTree as ET
import codecs
import os
import re
import copy
import nltk
from nltk.corpus import wordnet as wn
import pickle

check_word_list = {'NNS', 'VBD', 'VBG', 'VBN'}


# xmlファイルからタグを外してテキスト部分のみを取り出す
def strip_tags(xml_file, file):
    tree = ET.parse('XML_files/' + xml_file)
    root = tree.getroot()

    # Mathタグの除去
    for child in root:
        for p in child.findall('{http://dlmf.nist.gov/LaTeXML}p'):
            for math in p.findall('{http://dlmf.nist.gov/LaTeXML}Math'):
                for x_math in math.findall('{http://dlmf.nist.gov/LaTeXML}XMath'):
                    math.remove(x_math)
                    tree.write('XML_files/' + xml_file)

    for child in root:
        for equation in child.findall('{http://dlmf.nist.gov/LaTeXML}equation'):
            child.remove(equation)
            tree.write('XML_files/' + xml_file)

    notags = ET.tostring(root, method='text')
    notags = notags.decode('utf8')
    text_list = notags.split('\n')
    text = ''
    for t in text_list:
        text += t + ' '

    word_list = text.split(' ')
    word_list = [word for word in word_list if word is not '']
    copy_word_list = copy.copy(word_list)
    # remove_flag = 0
    # nl_flag = 0
    clean_text = ''
    remove_flag = 0
    for w in copy_word_list:
        ################################################正規表現################################################
        pattern1 = '.*\[.*'  # 関連文献の番号消去用正規表現1
        pattern2 = '.*\]'  # 関連文献の番号消去用正規表現2
        pattern_sym = '\&#.*;'  # 元記号削除用正規表現
        pattern_link = '.+\-.+'  # 結合要素を含む単語削除用表現
        pattern_url = '(https).*'  # URL削除用表現
        pattern_cpt = '\d+(\.\d*)*\,*'  # 章番号削除用正規表現
        pattern_bra1 = '.*\(.*'
        pattern_bra2 = '.*\)'
        pattern_word_link = '.*\-'
        ########################################################################################################
        m_cpt = re.fullmatch(pattern_cpt, str(w))
        if m_cpt is not None:
            word_list[word_list.index(w)] = word_list[word_list.index(w)].replace(w[m_cpt.start():m_cpt.end()],
                                                                                  'NUMBER')
            # word_list[count] = "NUMBER"
        # copy_word_list = copy.copy(word_list)

        # 結合要素(-)をもつ単語の削除
        m_link = re.search(pattern_link, str(w))
        if m_link is not None:
            word_list[word_list.index(w)] = word_list[word_list.index(w)].replace(w[m_link.start():m_link.end()],
                                                                                  'LINKWORD')
            # word_list[count] = "LINKWORD"
        # copy_word_list = copy.copy(word_list)

        # 元記号を取り除く処理
        m_ite = re.search(pattern_sym, str(w))
        if m_ite is not None:
            word_list[word_list.index(w)] = word_list[word_list.index(w)].replace(w[m_ite.start():m_ite.end()],
                                                                                  'SYMBOL')

        # URL要素の削除
        m_url = re.search(pattern_url, str(w))
        if m_url is not None:
            word_list[word_list.index(w)] = word_list[word_list.index(w)].replace(w[m_url.start():m_url.end()], 'URL')
            # word_list[count] = "URL"
        # copy_word_list = copy.copy(word_list)

        # 関連番号を取り除く処理
        m1 = re.match(pattern1, str(w))
        m2 = re.match(pattern2, str(w))
        # m1 = re.search(pattern1, str(w))
        # m2 = re.search(pattern2, str(w))

        # wに'['が含まれていないかを確認する
        if remove_flag == 0:
            if m1 is not None:
                if m2 is not None:
                    word_list[word_list.index(w)] = word_list[word_list.index(w)].replace(w[m2.start():m2.end()],
                                                                                          'SBRACKETS')
                else:
                    word_list.remove(w)
                    remove_flag = 1
        else:
            if m2 is not None:
                word_list.remove(w)
                word_list[word_list.index(w)] = word_list[word_list.index(w)].replace(w[m2.start():m2.end()],
                                                                                      'SBRACKETS')
                remove_flag = 0
            else:
                word_list.remove(w)

        if w != '':
            if remove_flag == 0:
                clean_text = clean_text + ' '.join(w) + ' '

        # copy_word_list = copy.copy(word_list)
        # last_index = len(word_list) - 1

        # 文章の途中で改行が挟まった場合につく'-'を取り除く処理
        m_word_link = re.fullmatch(pattern_word_link, str(w))
        if m_word_link is not None:
            link_word = word_list[word_list.index(w)].replace('-', '') + word_list[word_list.index(w) + 1]
            if wn.synsets(link_word):
                word_list[word_list.index(w)] = word_list[word_list.index(w)].replace(
                    w[m_word_link.start():m_word_link.end()],
                    link_word)
                word_list[word_list.index(w) + 1].remove()
            else:
                word_list[word_list.index(w)] = word_list[word_list.index(w)].replace(
                    w[m_word_link.start():m_word_link.end()],'LINKWORD')
                word_list[word_list.index(w) + 1].remove()

    ##################################単語辞書作成##########################################
    text_info = nltk.word_tokenize(clean_text)  # 単語の分かち書き
    pos = nltk.pos_tag(text_info)  # 単語の情報
    # print(pos)
    # stemmer = nltk.stem.PorterStemmer()  # 原型処理を持つ関数へのアクセス
    # 特定の単語の原型化処理
    for pos_list_num in range(len(pos)):
        if pos[pos_list_num][1] in check_word_list:
            text_info[pos_list_num] = wn.morphy(text_info[pos_list_num])
    # print(text_info)
    word_dict = []  # テキスト中に出てくる単語のリスト（重複あり）
    for word in text_info:
        if word is not None:
            if word.isalpha() is True and wn.synsets(word):
                word_dict.append(word)
    # print(word_dict)

    # 辞書ファイルへの書き込み操作
    if os.path.isfile('./changed_dictionary.txt'):
        with open('./changed_dictionary.txt', mode='r') as f:
            exist_word_list = [s.strip() for s in f.readlines()]
        linked_list = word_dict + exist_word_list
        linked_set = set(linked_list)
        text_word_list = sorted(linked_set)
    else:
        text_word_list = sorted(set(word_dict))

    with open('./changed_dictionary.txt', mode='w') as f:
        f.writelines('\n'.join(list(text_word_list)))
    # print(word_dict_sorted)
    ######################################################################################
    with codecs.open('TXT_files\\' + file + '.txt', 'w', 'utf8') as f:
        f.write(clean_text)


if not os.path.isdir("XML_files"):
    subprocess.Popen("mkdir XML_files", shell=True)

if not os.path.isdir("TXT_files"):
    subprocess.Popen("mkdir TXT_files", shell=True)

if not os.path.isdir("TEX_files"):
    subprocess.Popen("mkdir TEX_files", shell=True)

#########################################################################################
# コマンドラインからInftyReaderを使ってLatexファイルを作成
# pdf_files = glob.glob("PDF\*.pdf")
# for f_count in range(len(pdf_files)):
#     pdf_files[f_count] = pdf_files[f_count].replace('PDF\\', '')
#
# d = os.path.dirname(os.path.abspath(__file__))
# for pf in pdf_files:
#     cmd = "Infty \"" + d + "\PDF\" " + pf + " -f tex -o \"" + d + "\TEX_files\""
#     # print(cmd)
#     popen = subprocess.Popen(cmd, shell=True)
#     popen.wait()
#     # 中間素材の削除処理
#     png_files = glob.glob("PDF\*.png")
#     for png in png_files:
#         cmd = "del " + png
#         popen = subprocess.Popen(cmd, shell=True)
#         popen.wait()
#     iml = pf.replace(".pdf", "") + ".iml"
#     cmd = "del TEX_files\\" + iml
#     popen = subprocess.Popen(cmd, shell=True)
#     popen.wait()
#     iml_x = pf.replace(".pdf", "") + ".imlx"
#     cmd = "del TEX_files\\" + iml_x
#     popen = subprocess.Popen(cmd, shell=True)
#     popen.wait()
#########################################################################################

files = glob.glob("TEX_files\*.tex")
for f_count in range(len(files)):
    files[f_count] = files[f_count].replace('TEX_files\\', '')
    files[f_count] = files[f_count].replace('.tex', '')

print("ディレクトリ内のすべてのファイルを変換しますか？Y/N")
change_flag = input()
if change_flag == 'Y' or change_flag == 'y':
    for fn in files:
        fr = fn + ".tex"
        to = fn + ".xml"

        cmd = "latexml --noparse --quiet --destination=XML_files/" + to + " TEX_files/" + fr
        # print(cmd)
        popen = subprocess.Popen(cmd, shell=True)
        popen.wait()
        strip_tags(to, fn)
        with open('./changed_dictionary.txt', mode='r') as f:
            all_word_list = [s.strip() for s in f.readlines()]
        DIC = {}
        for w_num in range(len(all_word_list)):
            DIC[all_word_list[w_num]] = w_num
        with open('./changed_dictionary.pickle', mode='wb') as f:
            pickle.dump(DIC, f)

elif change_flag == "N" or change_flag == "n":
    print("変換するファイルの名前を入力(拡張子は含まず入力):")
    fn = input()
    fr = fn + ".tex"
    to = fn + ".xml"

    if os.path.isfile("TEX_files\\" + fr):
        cmd = "latexml --quiet --destination=XML_files/" + to + " TEX_files/" + fr
        # print(cmd)
        popen = subprocess.Popen(cmd, shell=True)
        popen.wait()
        strip_tags(to, fn)
    else:
        print("指定した名前のtexファイルが存在していません。")

sys.exit(0)
