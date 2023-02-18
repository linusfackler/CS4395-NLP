# Linus Fackler - LXF210001
# CS4395.001
# Dr. Mazidi
#
# This program...
#

import sys
import os
import nltk
nltk.download('punkt')
from nltk.book import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


def main():

    if len(sys.argv) < 2:
        print("Please enter a filename as a system argument!")
        print("Exiting now")
        sys.exit()

    else:
        filepath = sys.argv[1]

        textfile = open(filepath, "r")
        text = textfile.read()
        textfile.close()

        tokens = word_tokenize(text)

        print("\nThe number of tokens in text: ", len(tokens))

        tokenSet = set(tokens)
        print("\nThe number of unique tokens in text:", len(tokenSet))

        print("\nThe first 5 unqieu tokens in text:", sorted(tokenSet)[:5])

        # get rid of punctuation and stopwords
        tokens = [t for t in tokens if t.isalpha() and t not in stopwords.words('english')]

        print("\nThe number of important words in text:", len(tokens))
        print("\nThe number of unique important words in text:", len(set(tokens)))
        print("\nThe first 10 unique important words in text:", tokens[:10])

if __name__ == '__main__':
    main()  # call main function