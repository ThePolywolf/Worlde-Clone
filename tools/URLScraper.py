import requests
from bs4 import BeautifulSoup
import sys


word_txt_file = "all_8_words.txt"
URL = "https://www.allscrabblewords.com/8-letter-words/"
response = requests.get(URL)

if response.status_code == 200:
    page = response.text
else:
    print("Failed Fetch")
    exit()
print("> URL Accessed")

soup = BeautifulSoup(page, "html.parser")
parent_element = soup.find("ul", class_="list-inline")

# grab all items from the list
if parent_element:
    print("> List Found")

    file = open(word_txt_file, 'w')
    list_items = parent_element.find_all("li")
    print("> List Gathered")

    count = 0
    sys.stdout.write("> 0 items tracked")

    for item in list_items:
        word = item.find("a")
        word_str = word.contents[0]
        file.write(str(word_str) + "\n")
        
        count += 1
        track_text = "> " + str(count) + " words tracked | Current Word: " + str(word_str)
        sys.stdout.write("\r" + track_text)
    
    file.close()
else:
    print("Parent not found")
    exit()

# new line
print("")
