# Linus Fackler - LXF210001
# CS4395.001
# Dr. Mazidi
#
# Portfolio Chapter 8: Ngrams
# Program 1
#
# This program reads 3 input files, processes the text, and creates unigrams and bigrams for each text.
# It then saves each dictionary as a pickle.
#

import sys
from nltk.tokenize import word_tokenize as tokenize
from nltk.util import ngrams
import pickle

def create_dictionaries(filepath):
    try:
        textfile = open(filepath, "r")      # open text file if it exists
    except:
        print("Error: File", filepath , "does not exist. Check file path and try again.")
        sys.exit()
    
    text = textfile.read()              # read raw text
    textfile.close()                    # close text file

    text = text.replace("\n", "")       # remove newlines

    token_text = tokenize(text)         # tokenize text

    bigrams = list(ngrams(token_text, 2))       # create bigram from tokened text
    unigrams = list(ngrams(token_text, 1))      # create unigram from tokened text

    bigram_dict = {}                            # create bigram dictionary
    for b in bigrams:
        bigram_dict[b] = bigram_dict.get(b, 0) + 1      # count key

    unigram_dict = {}                           # create unigram dictionary
    for u in unigrams:
        unigram_dict[u] = unigram_dict.get(u, 0) + 1    # count key

    return unigram_dict, bigram_dict

def main():
    if len(sys.argv) < 4:       # check for 3 filenames
        print("Please enter 3 filenames as a system argument!")
        print("Example:")
        print("\tpython3 create_ngrams.py file1.ext file2.ext file3.ext")
        print("Exiting now")
        sys.exit()

    else:
        filepaths = [sys.argv[1], sys.argv[2], sys.argv[3]]

        for path in filepaths:
            if "English" in path:
                unigram_eng, bigram_eng = create_dictionaries(path)    # create unigram & bigram for english
            elif "French" in path:
                unigram_fr, bigram_fr = create_dictionaries(path)
            elif "Italian" in path:
                unigram_ita, bigram_ita = create_dictionaries(path)
            else:
                print("Language not recognized. Check input file.")
                sys.exit()

        pickle.dump(unigram_eng, open('pickles/unigram_eng.p','wb'))        # pickle english unigram
        pickle.dump(bigram_eng, open('pickles/bigram_eng.p','wb'))          # pickle english bigram

        pickle.dump(unigram_fr, open('pickles/unigram_fr.p','wb'))          # pickle french unigram
        pickle.dump(bigram_fr, open('pickles/bigram_fr.p','wb'))            # pickle french bigram

        pickle.dump(unigram_ita, open('pickles/unigram_ita.p','wb'))        # pickle italian unigram
        pickle.dump(bigram_ita, open('pickles/bigram_ita.p','wb'))          # pickle italian bigram


if __name__ == '__main__':
    main()  # call main function