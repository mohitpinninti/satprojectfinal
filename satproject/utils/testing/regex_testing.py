# taken from https://www.tutorialspoint.com/file-searching-using-python#:~:text=Python%20can%20search%20for%20file,dirpath%2C%20dirnames%2C%20and%20filenames.


import os
import re

def find_band(ending_name, search_path):
    result = []

# Walking top-down from the root
    for root, dir, files in os.walk(search_path):
        for file in files:
            somename = re.search(".*" + ending_name, file)
            if somename:
                result.append(os.path.join(root, somename[0]))
    return result

str = ""

print(find_band("B01.jp2", "C:\\Users\\pinni\\OneDrive\\Desktop\\ADM\\satprojectFromTweetSent"))