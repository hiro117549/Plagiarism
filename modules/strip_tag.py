# xmlファイルを操作するモジュールです
# xmlElementTreeを使用してxmlファイル中に存在するテキスト部分のみを抽出し、
# 正規表現を利用して不要な文字列を取り除きます。
# その後テキストファイルにいじったテキストを書きだします。
import xml.etree.ElementTree as ET
import codecs
import re
import copy


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

################################################正規表現################################################
    pattern1 = '.*\[.*'             # 関連文献の番号消去用正規表現1
    pattern2 = '.*\]'               # 関連文献の番号消去用正規表現2
    pattern_sym = '\&#.*;'          # 元記号削除用正規表現
    pattern_link = '.*\-.+'         # 結合要素を含む単語削除用表現
    pattern_url = '(https).*'       # URL削除用表現
    pattern_cpt = '\d+(\.\d*)*\,*'  # 章番号削除用正規表現
    pattern_word_link = '.*\-'
########################################################################################################
    remove_flag = 0
    for t in text_list:
        nl_flag = 0
        word_list = t.split(' ')
        word_list = [word for word in word_list if word is not '']
        copy_word_list = copy.copy(word_list)

        count = 0
        for w in copy_word_list:
            m_cpt = re.fullmatch(pattern_cpt, str(w))
            if m_cpt is not None:
                word_list[count] = word_list[count].replace(w[m_cpt.start():m_cpt.end()], 'NUMBER')
                # word_list[count] = "NUMBER"
            count += 1
        copy_word_list = copy.copy(word_list)

        # 結合要素(-)をもつ単語の削除
        count = 0
        for w in copy_word_list:
            m_link = re.search(pattern_link, str(w))
            if m_link is not None:
                word_list[count] = word_list[count].replace(w[m_link.start():m_link.end()], 'LINKWORD')
            count += 1
        # copy_word_list = copy.copy(word_list)

        # 文章の途中で改行が挟まった場合につく'-'を取り除く処理
        last_index = len(word_list) - 1
        if last_index >= 1:
            last_word = word_list[last_index]
            if re.fullmatch(pattern_word_link, str(last_word)) is not None:
                nl_flag = 1
                word_list[last_index] = word_list[last_index].replace('-', '')
        copy_word_list = copy.copy(word_list)

        # 元記号を取り除く処理
        count = 0
        for w in copy_word_list:
            m_ite = re.search(pattern_sym, str(w))
            if m_ite is not None:
                word_list[count] = word_list[count].replace(w[m_ite.start():m_ite.end()], '')
            count += 1
        copy_word_list = copy.copy(word_list)

        # URL要素の削除
        count = 0
        for w in copy_word_list:
            m_url = re.search(pattern_url, str(w))
            if m_url is not None:
                word_list[count] = word_list[count].replace(w[m_url.start():m_url.end()], 'URL')
            count += 1
        copy_word_list = copy.copy(word_list)

        # 関連番号を取り除く処理
        count = 0
        for w in copy_word_list:
            m1 = re.match(pattern1, str(w))
            m2 = re.match(pattern2, str(w))

            # wに'['が含まれていないかを確認する
            if remove_flag == 0:
                if m1 is not None:
                    if m2 is not None:
                        word_list[count] = word_list[count].replace(w[m2.start():m2.end()], 'SBRACKETS')
                    else:
                        word_list.remove(w)
                        count -= 1
                        remove_flag = 1
            else:
                if m2 is not None:
                    word_list.remove(w)
                    count -= 1
                    # word_list[count] = word_list[count].replace(w[m2.start():m2.end() + 1], 'SBRACKETS')
                    remove_flag = 0
                else:
                    count -= 1
                    word_list.remove(w)
            count += 1

        if len(word_list) is not 0:
            if nl_flag == 0 and remove_flag == 0:
                text = text + ' '.join(word_list) + ' '
            else:
                text = text + ' '.join(word_list)

        # copy_word_list = copy.copy(word_list)
        # last_index = len(word_list) - 1

    # text = text.decode('utf8')
    with codecs.open('TXT_files\\'+file+'.txt', mode='w') as f:
        f.write(text)
    return text
