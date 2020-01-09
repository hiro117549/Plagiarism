# k2pdfoptを使用して論文の1ページ目のみを確実に1コラムの文章にする(なってるはず)
import subprocess


def k2pdfopt_use(file_name):
    print(file_name)
    cmd = "K2pdfopt " + file_name + " -wrap- -n -c -o PDF\k2opt_files\k2opt_%b -odpi 600 -h 29.7cm -w 21cm -p 1"
    popen = subprocess.Popen(cmd, shell=True)
    popen.wait()
