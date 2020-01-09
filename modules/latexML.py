import subprocess
import os
from modules import strip_tag


def make_xml(fn):
    # os.chdir('..')
    fr = fn + ".tex"
    to = fn + ".xml"
    cmd = "latexml --noparse --quiet --destination=XML_files/" + to + " TEX_files/" + fr
    # print(cmd)
    popen = subprocess.Popen(cmd, shell=True)
    popen.wait()
    if not os.path.isfile("XML_files/" + fn + ".xml"):
        return 0
    text_since_2p = strip_tag.strip_tags(to, fn)
    return text_since_2p


def make_1p_xml(fn):
    k_fr = "k2opt_" + fn + ".tex"
    if not os.path.isfile("TEX_files/k2opt_files" + fn):
        return 0
    k_to = "k2opt_" + fn + ".xml"
    cmd = "latexml --noparse --quiet --destination=XML_files/k2opt_files/" + k_to + " TEX_files/k2opt_files/" + k_fr
    # print(cmd)
    popen = subprocess.Popen(cmd, shell=True)
    popen.wait()
    text_1p = strip_tag.strip_tags("k2opt_files/" + k_to, "k2opt_" + fn)
    return text_1p