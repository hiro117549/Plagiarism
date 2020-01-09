import sys
import subprocess
import glob
import os
import pickle
from modules import make_word_dic
from modules import option_parser
from modules import Latex
from modules import latexML


if __name__ == '__main__':
    args = option_parser.get_option()
    # ファイル作成領域の下準備
    if not os.path.isdir("XML_files"):
        subprocess.Popen("mkdir XML_files", shell=True)

    if not os.path.isdir("TXT_files"):
        subprocess.Popen("mkdir TXT_files", shell=True)

    if not os.path.isdir("TEX_files"):
        subprocess.Popen("mkdir TEX_files", shell=True)

    if not os.path.isdir("TXT_files/change_root_file"):
        subprocess.Popen("mkdir TXT_files\change_root_file", shell=True)

    if not os.path.isdir("TXT_files/exchanged_files"):
        subprocess.Popen("mkdir TXT_files\exchanged_files", shell=True)

    if not os.path.isdir("TEX_files/k2opt_files"):
        subprocess.Popen("mkdir TEX_files/k2opt_files", shell=True)

    if not os.path.isdir("XML_files/k2opt_files"):
        subprocess.Popen("mkdir XML_files/k2opt_files", shell=True)

    # コマンドラインからInftyReaderを使ってLatexファイルを作成
    # if not args.sIR:
    #     print('start Infty')
    #     Latex.make_Latex(args.endfile)
    if args.rd:
        if os.path.isfile("dictionary.txt"):
            cmd = 'del dictionary.txt dictionary.pickle'
            # print(cmd)
            popen = subprocess.Popen(cmd, shell=True)
            popen.wait()

    # Latexのファイルをxmlファイルに変換し、テキストの抽出を行うメインの処理
    files = glob.glob("PDF\*.pdf")

    for pdf_file in files[0:args.endfile]:
        if args.sIR is False:
            Latex.make_latex(pdf_file)
        fn = (pdf_file.replace('PDF\\', '')).replace('.pdf', '')
        # print(fn)

        if args.ntex:
            text = latexML.make_xml(fn)
        else:
            text_1p = latexML.make_1p_xml(fn)
            if text_1p == 0:
                text = latexML.make_xml(fn)
                if text == 0:
                    continue
            else:
                text_since_2p = latexML.make_xml(fn)
                if text_since_2p is 0:
                    continue
                text = text_1p + text_since_2p

        make_word_dic.make_word_dic(text, fn, args.ew)
        # 単語索引作成(txt形式)
        with open('./dictionary.txt', mode='r') as f:
            all_word_list = [s.strip() for s in f.readlines()]

        # 辞書ファイル作成(pickle形式)
        DIC = {}
        for w_num in range(len(all_word_list)):
            DIC[all_word_list[w_num]] = w_num
        with open('./dictionary.pickle', mode='wb') as f:
            pickle.dump(DIC, f)

    sys.exit(0)
