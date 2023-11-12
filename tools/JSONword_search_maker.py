from enum import Enum
import sys  # for updating percentages as processing occurs
import json

JSON_file = "_word_search_tree.json"
threshold = 20


class word_tree():    
    def __init__(self, prefix: str = ''):
        self.prefix = prefix
        self.depth = len(self.prefix)
        self.count = 0
        self.sub_words = []
        self.stores_words = True

    def add_word(self, word: str):
        self.count += 1

        if self.stores_words:
            self.sub_words.append(word)

            # subdivide contents if contents exceed threshold
            if len(self.sub_words) > threshold:
                self.stores_words = False
                
                # initializing
                replacement_group = []
                new_group = word_tree(self.sub_words[0][:self.depth + 1])
                
                # move each word into subgroup
                for word in self.sub_words:
                    # create new group when ready
                    if not new_group.match_prefix(word):
                        replacement_group.append(new_group)
                        new_group = word_tree(word[:self.depth + 1])
                    new_group.add_word(word)
                replacement_group.append(new_group)
                
                # replace sub_words with list of sub_words
                self.sub_words = replacement_group
        else:
            # add to subgroup if exists
            for subgroup in self.sub_words:
                if subgroup.match_prefix(word):
                    subgroup.add_word(word)
                    return
            
            # create subgroup if it doesn't exist
            new_group = word_tree(word[:self.depth + 1])
            new_group.add_word(word)
            self.sub_words.append(new_group)
    
    def match_prefix(self, word: str) -> bool:
        return word[:self.depth] == self.prefix

def word_tree_to_dict(tree: word_tree):
    if tree.stores_words:
        # returns list of words
        tree_list = []
        for word in tree.sub_words:
            tree_list.append(word)
        return [tree.count, tree_list]
    else:
        tree_dict = {}
        # defines keys
        for sub_dict in tree.sub_words:
            tree_dict[sub_dict.prefix] = word_tree_to_dict(sub_dict)

            sys.stdout.write('\r> %s prefix converted    -' % sub_dict.prefix)

        return [tree.count, tree_dict]

# run through all 3-7 length word documents
for n in range(2, 9, 1):
    txt_path = "all_"+str(n)+"_words.txt"

    # access words
    print("Accessing txt file")
    stored_txt = open(txt_path)

    # store txt file data
    print("Storing raw txt data")
    words = stored_txt.readlines()

    # calculate # of words once
    total = len(words)

    # remove new lines
    for i in range(0, total, 1):
        new_word = words[i].replace('\n', '')
        words[i] = new_word
        sys.stdout.write('\r> %s/%s stored | %s' %(str(i + 1), str(total), new_word))
    print("")

    # initialize word tree
    print("Initializing word tree")
    tree = word_tree()

    # store words in tree
    print("Storing words in tree")
    for i in range(0, total, 1):
        tree.add_word(words[i])
        sys.stdout.write('\r> %s/%s stored | %s' %(str(i + 1), str(total), words[i]))
    print('')

    # turn word_trees into a dictionary
    print("Converting to Dictionary")
    dictionary = word_tree_to_dict(tree)
    print("\n> Finished converting")

    # store dictionary to JSON
    print("Storing dict to JSON")
    json_file = open(str(n)+JSON_file, 'w')
    json.dump(dictionary, json_file, indent=4)
    json_file.close()
    print("> Data stored")
    print("")