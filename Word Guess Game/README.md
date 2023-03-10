# Portfolio Chapter 5: Word Guess Game

[Python File](https://github.com/linusfackler/CS4395-NLP/blob/main/Word%20Guess%20Game/main.py)
|
[Text File](https://github.com/linusfackler/CS4395-NLP/blob/main/Word%20Guess%20Game/anat19.txt)

## What the program does
This program takes input files, processes the text, and creates unigrams and bigrams for each text. These are used to train an n-gram model to detect the language in a given text
Line by line it classifies the test file as either English, French, or Italian.
It then shows the overall accuracy of the model, as well as incorrectly classified lines of text.

## How to run it
Your machine needs to have Python3 installed.
Navigate to the script file in your terminal and enter:
```
To create unigrams & bigrams:
python3 create_ngrams.py file1.ext file2.ext file3.ext

For example:
python3 create_ngrams.py data/LangId.train.English data/LangId.train.French data/LangId.train.Italian


To test on existing text:
python3 ngram_prob.py test.ext val.ext

For example:
python3 ngram_prob.py data/LangId.test data/LangId.sol
```
