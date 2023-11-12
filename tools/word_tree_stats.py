import sys
import json


file_path = "_word_search_tree.json"
str_len = 9

for n in range(2, 9, 1):
    path = str(n) + file_path

    json_file = open(path, 'r')
    dictionary = json.load(json_file)
    json_file.close()

    print("%s Word Length total: %s" % (str(n), str(dictionary[0])))
    count = 0
    for key in dictionary[1]:
        count += 1
        if count > 13:
            count -= 13
            print("")
        string = "%s:%s " %(key, dictionary[1][key][0])
        for i in range(len(string), str_len, 1):
            string += " "
        sys.stdout.write(string)
    
    print("\n")