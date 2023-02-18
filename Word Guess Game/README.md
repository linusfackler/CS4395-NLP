# Portfolio Chapter 5: Word Guess Game

[Python File](https://github.com/linusfackler/CS4395-NLP/blob/main/Word%20Guess%20Game/main.py)
|
[Text File](https://github.com/linusfackler/CS4395-NLP/blob/main/Word%20Guess%20Game/anat19.txt)

## What the program does
This program lets the user guess a word from one of the top 50 most common nouns in the user-input text. The text will first be tokenized and preprocessed.
The game starts with a score of 5 and the user gets to guess a letter. If the guessed letter is in the word, the user will get 1 point. If not, 1 point will be deducted.
The game ends if the user enters '!' or the score falls below 0.

## How to run it
Your machine needs to have Python3 installed.
Navigate to the script file in your terminal and enter:
```
python3 main.py <data path>

For example:
python3 main.py "anat19.txt"
```
