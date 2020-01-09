# InftyReaderを使用するモジュールです。
# InftyReaderを使用して、PDFをtexに変換したりその時出てくる中間素材を消したりするやつ
import glob
import subprocess
import os
import PyPDF2
from modules import k2pdfopt


def make_Latex(end_page):
    pdf_files = glob.glob("PDF\*.pdf")
    d = os.path.dirname(os.path.abspath(__file__)).replace('\\modules', '\\PDF\\k2opt_files')
    if end_page == -1 or end_page > len(pdf_files):
        end_page = len(pdf_files)

    for f_count in range(end_page):
        pdf_file = pdf_files[f_count]
        k2opt_pdf_file = pdf_file.replace('PDF\\', 'k2opt_')
        pdfFileObj = open(pdf_file, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        page_num = pdfReader.numPages
        k2pdfopt.k2pdfopt_use(pdf_file)

        # 変換された１ページ目のみを変換する
        cmd = "Infty \"" + d + "\" " + k2opt_pdf_file + " -f tex -o \"" + d.replace('\\PDF\\k2opt_files', '') + "\\TEX_files\\k2opt_files\""
        # print(cmd)
        popen = subprocess.Popen(cmd, shell=True)
        popen.wait()

        # ２ページ目以降も変換する
        cmd = "Infty \"" + d.replace('\\k2opt_files', '') + "\" " + pdf_file.replace('PDF\\', '') + " -f tex -o \"" + d.replace('\\PDF\\k2opt_files', '') + "\\TEX_files\" -StartPage 2 -endPage " + str(page_num)
        # print(cmd)
        popen = subprocess.Popen(cmd, shell=True)
        popen.wait()

        # 中間素材の削除処理
        png_files = glob.glob("PDF\k2opt_files\*.png")
        for png in png_files:
            cmd = "del " + png
            popen = subprocess.Popen(cmd, shell=True)
            popen.wait()
        png_files = glob.glob("PDF\*.png")
        for png in png_files:
            cmd = "del " + png
            popen = subprocess.Popen(cmd, shell=True)
            popen.wait()

        iml_files = glob.glob("TEX_files\*.iml")
        for iml in iml_files:
            # iml = file_name.replace(".pdf", "") + ".iml"
            cmd = "del " + iml
            popen = subprocess.Popen(cmd, shell=True)
            popen.wait()
        iml_x_files = glob.glob("TEX_files\*.imlx")
        for iml_x in iml_x_files:
            # iml_x = file_name.replace(".pdf", "") + ".imlx"
            cmd = "del " + iml_x
            popen = subprocess.Popen(cmd, shell=True)
            popen.wait()

        k2_iml_files = glob.glob("TEX_files\k2opt_files\*.iml")
        for k2_iml in k2_iml_files:
            # iml = file_name.replace(".pdf", "") + ".iml"
            cmd = "del " + k2_iml
            popen = subprocess.Popen(cmd, shell=True)
            popen.wait()
        iml_x_files = glob.glob("TEX_files\k2opt_files/*.imlx")
        for k2_iml_x in iml_x_files:
            # iml_x = file_name.replace(".pdf", "") + ".imlx"
            cmd = "del " + k2_iml_x
            popen = subprocess.Popen(cmd, shell=True)
            popen.wait()


def make_latex(pdf_file):
    d = os.path.dirname(os.path.abspath(__file__)).replace('\\modules', '\\PDF\\k2opt_files')

    k2opt_pdf_file = pdf_file.replace('PDF\\', 'k2opt_')
    pdfFileObj = open(pdf_file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    page_num = pdfReader.numPages
    k2pdfopt.k2pdfopt_use(pdf_file)

    # 変換された１ページ目のみを変換する
    cmd = "Infty \"" + d + "\" " + k2opt_pdf_file + " -f tex -o \"" + d.replace('\\PDF\\k2opt_files',
                                                                                    '') + "\\TEX_files\\k2opt_files\""
    # print(cmd)
    popen = subprocess.Popen(cmd, shell=True)
    popen.wait()

    # ２ページ目以降も変換する
    cmd = "Infty \"" + d.replace('\\k2opt_files', '') + "\" " + pdf_file.replace('PDF\\',
            '') + " -f tex -o \"" + d.replace('\\PDF\\k2opt_files', '') + "\\TEX_files\" -StartPage 2 -endPage " + str(page_num)
    # print(cmd)
    popen = subprocess.Popen(cmd, shell=True)
    popen.wait()

    # 中間素材の削除処理
    png_files = glob.glob("PDF\k2opt_files\*.png")
    for png in png_files:
        cmd = "del " + png
        popen = subprocess.Popen(cmd, shell=True)
        popen.wait()
    png_files = glob.glob("PDF\*.png")
    for png in png_files:
        cmd = "del " + png
        popen = subprocess.Popen(cmd, shell=True)
        popen.wait()

    iml_files = glob.glob("TEX_files\*.iml")
    for iml in iml_files:
        # iml = file_name.replace(".pdf", "") + ".iml"
        cmd = "del " + iml
        popen = subprocess.Popen(cmd, shell=True)
        popen.wait()
    iml_x_files = glob.glob("TEX_files\*.imlx")
    for iml_x in iml_x_files:
        # iml_x = file_name.replace(".pdf", "") + ".imlx"
        cmd = "del " + iml_x
        popen = subprocess.Popen(cmd, shell=True)
        popen.wait()

    k2_iml_files = glob.glob("TEX_files\k2opt_files\*.iml")
    for k2_iml in k2_iml_files:
        # iml = file_name.replace(".pdf", "") + ".iml"
        cmd = "del " + k2_iml
        popen = subprocess.Popen(cmd, shell=True)
        popen.wait()
    iml_x_files = glob.glob("TEX_files\k2opt_files/*.imlx")
    for k2_iml_x in iml_x_files:
        # iml_x = file_name.replace(".pdf", "") + ".imlx"
        cmd = "del " + k2_iml_x
        popen = subprocess.Popen(cmd, shell=True)
        popen.wait()