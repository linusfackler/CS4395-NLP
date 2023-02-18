# Linus Fackler - LXF210001
# CS4395.001
# Dr. Mazidi
#
# This program...
#

import sys
import os
import nltk
#from nltk.book import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
# from random import seed
from random import randint


def guessingGame(most_common):
    points = 5
    word = most_common[randint(0, 49)]
    print("\n\n")
    print(word)
    underscore = ""
    for i in range(len(word)):
        underscore += '_'

    guesses = []

    while (points >= 0 ):
        for x in underscore:
            print(x, end=" ")

        if underscore == word:
            print("\nYou solved it!")
            print("\nCurrent score:", points)
            return
        
        print("\n\nEnter a letter:")

        guess = input()

        if guess == "!":
            exit()

        while guess in guesses:
            print("Already guessed this letter! Try again")
            guess = input()

        guesses.append(guess)

        if guess in word:
            points += 1
            print("Right! Score is", points)

            count_in_string = word.count(guess)

            idx = word.index(guess)

            underscore = underscore [:idx] + word[idx] + underscore[idx + 1:]

            if count_in_string > 1:
                oldIndex = idx        # save original index
                for i in range(count_in_string - 1):
                    idx = word[idx+1:].index(guess)
                    newIndex = oldIndex + idx + 1
                    underscore = underscore [:newIndex] + word[newIndex] + underscore[newIndex + 1:]
        

        else:
            points -= 1
            print("Sorry, guess again! Score is", points)


    


def preprocess(tokenText):
        tokens = [t.lower() for t in tokenText] # tokenizing lower case
    
        tokens = [t for t in tokens if t.isalpha() and t not in stopwords.words('english') and len(t) > 5]
        # get rid of punctuation, stopwords, and tokens with length <= 5

        # get lemmas
        wnl = WordNetLemmatizer()
        lemmas = [wnl.lemmatize(t) for t in tokens]

        # get unique lemmas
        unique_lemmas = list(set(lemmas))

        tags = nltk.pos_tag(unique_lemmas)
        print("\nFirst 20 unique lemmas tagged:", tags[:20])

        is_noun = lambda pos: pos[:2] == "NN"
        nouns = [word for (word, pos) in tags if is_noun(pos)]

        print("\nNumber of tokens:", len(tokens))
        print("Number of nouns:", len(nouns))

        return tokens, nouns



def main():

    if len(sys.argv) < 2:
        print("Please enter a filename as a system argument!")
        print("Exiting now")
        sys.exit()

    else:
        filepath = sys.argv[1]

        textfile = open(filepath, "r")      # open text file
        text = textfile.read()              # read raw text
        textfile.close()                    # close text file

        tokenText = word_tokenize(text)     # tokenize raw text
        tokenSet = set(tokenText)           # create set of tokens to get unique tokens

        # lexical diversity
        lexDiv = len(tokenSet) / len(tokenText)
        print("\nLexical Diversity: %.2f" % lexDiv) # lexical div. formatted to 2 dec places

        tokens, nouns = preprocess(tokenText)

        # create dictionary of {noun:count of noun in tokens}
        dic = {}
        for t in tokens:
            if t in nouns:
                if t in dic:
                    dic[t] += 1
                else:
                    dic[t] = 1

        # sort dic by count
        dic = dict(sorted(dic.items(), key=lambda item: item[1], reverse=True))
        # first 50 words (nouns with highest count)
        print("\n50 most common words:", dict(list(dic.items())[:50]))

        # first 50 words in list
        most_common = [n for n in dict(list(dic.items())[:50])]


        print("Let's play a word guessing game!")
        while(True):
            guessingGame(most_common)
            print("\nGuess another word")


if __name__ == '__main__':
    main()  # call main function