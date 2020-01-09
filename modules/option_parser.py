from argparse import ArgumentParser


def get_option():
    argparser = ArgumentParser(usage='main.py [-ew] [-sIR] [-end NUM] [-ntex] [-rd]',
                               prog='main',
                               epilog='end',
                               add_help=True)

    argparser.add_argument('-ew',
                           help='wordnetに登録されている単語のみを抽出し、文章に含まれる単語ではない文字列を辞書に登録しないようにする。',
                           action='store_true')

    argparser.add_argument('-sIR',
                           help='Infty Readerの処理をスキップしてlatexmlの処理からプログラムを動かす。'
                                '※ただし、Infty Readerで処理をした結果出力されたtexファイルを想定したプログラムであることに注意'
                                '  また、k2opt_files内にファイルが存在するとそのファイルを使って動くため次に出てくるsKpoオプション'
                                '  とのかみ合わせに注意。(1ページ目の内容が2回繰り返されるかも)',
                           action='store_true')

    # argparser.add_argument('-sKpo',
    #                        help='k2pdfoptを使用せず(1ページ目を変換せず)プログラムを動かす。時短になる。'
    #                             'このオプションを使用した場合、各ディレクトリ内のk2opt_filesディレクトリ内には何も作成されず、'
    #                             '1ページ目からInfty Readerの解析を行ったtexファイルが使用される。'
    #                             '各操作で作成されるファイルの作成場所はTEX_files,XML_files,TXT_files直下となる。'
    #                             '※k2pdfoptを使用してプログラムを動かしたときに作成されたtexファイル(2ページ目以降を変換やつ)は'
    #                             '  名前がかぶってしまうので消えてしまう。'
    #                             '※また、論文の1ページ目の上部中央にタイトルがあり2コラム論文であった場合、InftyReaderが正しく文章をつなげてくれない'
    #                             '  Infty Readerがつよつよになったら使ったほうがいいオプション。ちなみに作ってない！',
    #                        action='store_true')

    argparser.add_argument('-end','--endfile',type=int,
                           default=-1,
                           help='引数として与えられた数のpdfファイルに処理を行う。')

    argparser.add_argument('-ntex',
                           help='native tex',
                           action='store_true')

    argparser.add_argument('-rd',
                           help='reset dictionary',
                           action='store_true')
    return argparser.parse_args()