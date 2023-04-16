import os
import re
from zipfile import ZipFile
#from env import FILE_PATH
import utils


def find_band(ending_name, search_path):
    result = []

    #Walking top-down from the root
    for root, dir, files in os.walk(search_path):
        for file in files:
            somename = re.search(".*" + ending_name, file)
            if somename:
                #return os.path.join(root, somename[0])  # this can be used if only one result is going to be used
                result.append(os.path.join(root, somename[0]))
    return result[0]
#print(find_band("B01.jp2", FILE_PATH))

def unzip_file(filename):
    with ZipFile(os.path.join(FILE_PATH, filename + ".zip"), 'r') as zipped:
        zipped.extractall(FILE_PATH)
