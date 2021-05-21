from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, PunktSentenceTokenizer
from collections import Counter

import os, glob
import nltk 
import pprint

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
    stop_words.update(["'ve", "'s", 'new', "'m", 'from', 'today', 'subject', 're', 'edu', 'use', 'us', 've', 'let', ',','.', '-', ';', ':', "n't", "together", "'re", "great", "nice", "pretty", "much", "many", "thing", "things", "something", "somethings", "enough", '%'])

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
def main():
    # open the input folder with txt files
    os.chdir('../input')
    path_to_file = os.getcwd() + '/'
    words = {}

    # go through all files within the folder
    for filename in glob.glob(os.path.join(path_to_file, '*.txt')): #O(a)
        with open(filename, 'r') as f:
            script = read_file(filename)
            tagged_script = filter_text(script)
            
            #documents[os.path.basename(filename)] = filter_text(script)

            for tuples in tagged_script: #O(b)   -> O (a*b)
                interesting_word = tuples[0][0]
                # isolate just the word and append doc and count
                if interesting_word in words.keys():
                    # total sum nasil hesaplanacak yeni dictionary kullanmadan?
                    # update count and append file name, os.path.basename returns filename
                    words[interesting_word]['count'] += tuples[1]
                    words[interesting_word]['file'].append(os.path.basename(filename))
                else:
                    # initialize if not in dict
                    words[interesting_word]  = {'count': tuples[1], 'file': [os.path.basename(filename)]}

    pprint.pprint(sorted(words.items(), key=lambda x: (words[interesting_word]['count'])))


if __name__ == "__main__":
    main()

# isolate sentences, which would end with , . ; : ' " ] ) "