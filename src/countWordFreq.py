# author: Denem Orhun
# Script to parse documents and count occurrences of most common critical words
# This script considers Nouns and adjectives that occur most commonly to be important

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, PunktSentenceTokenizer
from collections import Counter

import os, glob
import nltk 
import pprint
from constants import APPENDUM

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Read file
def read_file(file):
    # get file
    try:
        script = ""

        with open(file, 'r') as program:
            script = program.read()
    except Exception as e:
        print(str(e))
    return script

# filter text
def filter_text(script):
    # convert file to lowercase 
    script = script.lower()

    # declare set of stopwords
    stop_words = set(stopwords.words('english'))
    stop_words.update(APPENDUM)

    # tokenize script into an array
    word_tokens = word_tokenize(script)

    # filter script based on stop words
    try:
        filtered_script = [w for w in word_tokens if not w in stop_words]
    # tag script with Nouns and Adjectives to isolate interesting words
        tagged_script = nltk.pos_tag(filtered_script)
        #pprint.pprint(tagged)

    except Exception as e:
        print(str(e))

    # tag interesting words with the occurrence count using Counter
    occurrences = Counter(tagged_script)
  
    # filter script by occurrences > 4
    tokenized_script = [el for el in occurrences.items() if el[1] > 6]
    #script = occurrences.most_common(15)
   
    # filter script by nouns and adjectives
    tokenized_script = [el for el in tokenized_script if el[0][1] == 'NN' or el[0][1] == 'NNS' or el[0][1] == 'JJ']

    return tokenized_script


# driver code
def read_files():
    # open the input folder with txt files
    os.chdir('../input')
    path_to_file = os.getcwd() + '/'
    

    words = {} 

    # go through all files within the folder
    for filename in glob.glob(os.path.join(path_to_file, '*.txt')): 
        with open(filename, 'r') as f:
            script = read_file(filename)
            tagged_script = filter_text(script)

        for tuples in tagged_script: 
            interesting_word = tuples[0][0]
            # isolate just the word and append doc and count
            if interesting_word in words.keys():
            # update count and append file name
                words[interesting_word]['count'] += tuples[1]
                words[interesting_word]['file'].append(os.path.basename(filename))
            # initialize if not in dict
            else:
                words[interesting_word]  = {'count': tuples[1], 'file': [os.path.basename(filename)]}

    
    pprint.pprint(sorted(words.items(), key=lambda x: (words[interesting_word]['count'])))


if __name__ == "__main__":
    read_files()

def main():
    pass