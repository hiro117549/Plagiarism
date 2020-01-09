import xml.etree.ElementTree as ET
import codecs


print("タグを外したいファイルの名前を入力(タグを含めて入力)")
file_name = input()
# 指定された
tree = ET.parse(file_name)
root = tree.getroot()

# Mathタグの削除
for child in root:
    # element = child.find('{http://dlmf.nist.gov/LaTeXML}p/{http://dlmf.nist.gov/LaTeXML}Math')
    for p in child.findall('{http://dlmf.nist.gov/LaTeXML}p'):
        for math in p.findall('{http://dlmf.nist.gov/LaTeXML}Math'):
            # if element is None:
            #     print(child.attrib)
            #     print('     has not Math tag')
            # else:
            # print(child.attrib)
            # print('     has Math tag.')
            print(child.attrib)
            print('     has Math tag.')
            p.remove(math)
            tree.write(file_name)

notags = ET.tostring(root, method='text')
notags = notags.decode('utf8')
with codecs.open('notags.txt', 'w', 'utf8') as f:
    f.write(notags)