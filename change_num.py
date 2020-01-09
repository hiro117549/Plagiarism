import glob
import copy
import pickle
from modules import open_pickle
# from nltk.corpus import wordnet as wn

# check_word_list = {'NNS', 'VBD', 'VBG', 'VBN', 'JJR', 'JJS', 'RBR', 'RBS'}

pickle_files = glob.glob('TXT_files/change_root_file/*.pickle')
print('Exchange all txt files? y/n')
exchange_flag = input()
word_dic = open_pickle.open_dic()

if exchange_flag == 'Y' or exchange_flag == 'y':
    for pf in pickle_files:                        # txt = TXT_files/change_root_file/***.txt
        string_list = open_pickle.open_list(pf)
        # print(string_list)
        copy_string_list = copy.copy(string_list)
        # print(string_list)
        for s in copy_string_list:
            s_index = string_list.index(s)
            if s is not None:
                if s.isalpha() is False:
                    del string_list[s_index]
                    continue
                for word in word_dic.keys():
                    if word == s:
                        string_list[s_index] = word_dic[word]
                        break
            else:
                del string_list[s_index]

        # print(string_list)
        file_name = pf.replace('TXT_files/change_root_file\\root_', '')  # file_name = ***.txt
        print(file_name)
        with open('TXT_files/exchanged_files/' + file_name.replace('.txt', '.pickle'), mode='wb') as f:
            pickle.dump(string_list, f)

        print(open_pickle.open_list('TXT_files/exchanged_files/' + file_name.replace('.txt', '.pickle')))

        # string = ''
        # with open('TXT_files/exchanged_files/' + file_name, mode='w') as f:
        #     for s in string_list:
        #         string = string + ' ' + str(s)
        #     f.write(string)
elif exchange_flag == 'N' or exchange_flag == 'n':
    print('input file name')