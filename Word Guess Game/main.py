# Linus Fackler - LXF210001
# CS4395.001
# Dr. Mazidi
#
# This program lets the user guess a word from one of the top 50 most common nouns in the
# user-input text. The text will first be tokenized and preprocessed.
#

import sys
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from random import randint


# this is the main game function of the program
def guessingGame(most_common):
    points = 5          # start game with 5 points
    word = most_common[randint(0, 49)]      # choose random word in range 0-49
    print("\n")
    underscore = ""
    for i in range(len(word)):
        underscore += '_'       # create string with _ for every letter

    guesses = []                # list to keep track of guessed letters

    while (points >= 0 ):       # while score is not negative
        for x in underscore:    # print current attempt (_ _ _ s _ for example)
            print(x, end=" ")

        if underscore == word:  # if current attempt equals word -> user wins
            print("\nYou solved it!")
            print("\nCurrent score:", points)
            return
        
        print("\n\nEnter a letter: ", end="")

        guess = input()         # get user input

        while guess in guesses:         # if letter was already guessed
            print("Already guessed this letter!")
            print("Here are the letters you already guessed:")
            print("Try again!\n")
            guesses.sort()              # sort guesses list
            for letter in guesses:      # print guesses list in alph. order
                print(letter,end="  ")
            print("\n")
            guess = input()             # get new input

        # if guess is more than 1 letter or not a letter at all (except for !)
        while guess != "!" and (len(guess) > 1 or not guess.isalpha()):
            print("You can only guess single letters! (a-zA-z)")
            print("Try again!")
            print()
            guess = input()

        if guess == "!":                # ! ends the game
            print("\nThanks for playin!\n")
            exit()

        guesses.append(guess)           # if guess is allowed, add to list

        if guess in word:               # if letter is in word
            points += 1                 # add point to score
            print("Right! Score is", points)

            # number of times letter is in string
            count_in_string = word.count(guess)

            # index of first time letter is in string
            idx = word.index(guess)

            # switch out underscore with correctly guessed letter
            underscore = underscore [:idx] + word[idx] + underscore[idx + 1:]

            # if letter appears > 1 time
            if count_in_string > 1:
                oldIndex = idx          # save original index
                for i in range(count_in_string - 1):
                    idx = word[idx+1:].index(guess)
                    newIndex = oldIndex + idx + 1
                    underscore = underscore [:newIndex] + word[newIndex] + underscore[newIndex + 1:]
                    # switch out letter with underscore for every other appearance of letter in word

        else:
            points -= 1             # wrong guess, subtract point from score
            if points >= 0:         # if score is not negative yet
                print("Sorry, guess again! Score is", points)

    print("\nSorry, you lost!\n")   # if score is negative, user lost
    print("The word was:", word)    # print word for user to see

# this function preprocesses the tokened Text
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


        print("\n\nLet's play a word guessing game!")
        print("\nEnter '!' to stop the game at any time!")
        while(True):
            guessingGame(most_common)
            print("\nGuess another word")
    
    exit()


if __name__ == '__main__':
    main()  # call main function