# Linus Fackler - LXF210001
# CS4395.001
# Dr. Mazidi
#
# Portfolio Chapter 8: Ngrams
# Program 2
#
# This program opens the pickles previously created in program 1. It then opens a test and validation file.
# Line by line it classifies the test file as either English, French, or Italian.
# It then shows the overall accuracy of the model, as well as incorrectly classified lines of text.
#

import sys
import pickle
from nltk.tokenize import word_tokenize as tokenize
from nltk.util import ngrams

def compute_probability(text, unigrams, bigrams, v):
        
    token_text = tokenize(text)         # tokenize text

    test_bigrams = list(ngrams(token_text, 2))       # create bigram from tokened text
    test_unigrams = list(ngrams(token_text, 1))      # create unigram from tokened text

    prob = 1        # starting prob

    for bigr in test_bigrams:
        b = bigrams[bigr] if bigr in bigrams else 0             # bigram count
        u = unigrams[bigr[0]] if bigr[0] in unigrams else 0     # unigram count of first word in bigram
        prob = prob * ((b + 1) / (u + v))                       # bigram probability with Laplace smoothing
    
    return prob

def main():

    # --- open pickles ---
    try:        # load pickles if they exist
        unigram_eng = pickle.load(open('pickles/unigram_eng.p', 'rb'))
        bigram_eng = pickle.load(open('pickles/bigram_eng.p', 'rb'))
        unigram_fr = pickle.load(open('pickles/unigram_fr.p', 'rb'))
        bigram_fr = pickle.load(open('pickles/bigram_fr.p', 'rb'))
        unigram_ita = pickle.load(open('pickles/unigram_ita.p', 'rb'))
        bigram_ita = pickle.load(open('pickles/bigram_ita.p', 'rb'))
    except:
        print("Couldn't find pickle.")
        print("Run create_ngrams.py first to create pickles.")
        sys.exit()

    # --- check sys args ---
    if len(sys.argv) < 3:       # check for 1 filename
        print("Please enter 2 filenames as a system argument!")
        print("Example:")
        print("\tpython3 ngram_prob.py test.ext val.ext")
        print("Exiting now")
        sys.exit()

    # --- open test file ---
    test = sys.argv[1]
    try:
        test_file = open(test, 'r')      # open text file if it exists
    except:
        print("Error: File", test , "does not exist. Check file path and try again.")
        exit()
    
    # --- open output file ---
    try:
        out_file = open('data/wordLangId.out', 'w')
    except:
        print("Could not open output file")
        sys.exit()
    
    # --- open validation file ---
    val = sys.argv[2]
    try:
        val_file = open(val, 'r')
        val_file_split = val_file.read().splitlines()
    except:
        print("Error: File", test , "does not exist. Check file path and try again.")
        exit()

    vocab = len(unigram_eng) + len(unigram_fr) + len(unigram_ita)       # total vocabulary size
    prob = [None] * 3           # empty list for each language probability
    num_correct = 0             # number of correct classifications
    i = 0                       # counter for val file

    for line in test_file:
        prob[0] = compute_probability(line, unigram_eng, bigram_eng, vocab) # prob for english
        prob[1] = compute_probability(line, unigram_fr, bigram_fr, vocab)   # prob for french
        prob[2] = compute_probability(line, unigram_ita, bigram_ita, vocab) # prob for italian

        max_index = prob.index(max(prob))           # index of max prob

        validation = val_file_split[i].split()      # validation file next line split into index & language

        if max_index == 0:                  # if max is english
            out_file.write("English\n")
            if validation[1] == "English":
                num_correct += 1
            else:
                print("Line", validation[0], "incorrectly classified as English, but is", validation[1])
        elif max_index == 1:                # if max is french
            out_file.write("French\n")
            if validation[1] == "French":
                num_correct += 1
            else:
                print("Line", validation[0], "incorrectly classified as French, but is", validation[1])
        else:                               # if max is italian
            out_file.write("Italian\n")
            if validation[1] == "Italian":
                num_correct += 1
            else:
                print("Line", validation[0], "incorrectly classified as Italian, but is", validation[1])
        i += 1

    accuracy = (num_correct / i) * 100          # accuracy of classifications
    print("\nAccuracy: %.2f" % accuracy, "%")    

if __name__ == '__main__':
    main()  # call main function