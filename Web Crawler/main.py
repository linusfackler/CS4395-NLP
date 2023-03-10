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

import os
import requests
from bs4 import BeautifulSoup
import re
import urllib.request
from nltk.tokenize import sent_tokenize, word_tokenize

def webCrawler(starter_url, url_file):
    wordsToCheck = ['pink', 'floyd']    # words to check if URL is relevant
    badWebsites = ['google', 'facebook', 'twitter', 'pinterest', 'flipboard']

    starter_website = 'loudersound'
    other_websites_count = 0

    counter = 0
    url_queue = []
    url_queue.append(starter_url)

    with open(url_file, 'w') as f:
        while other_websites_count < 5:
            test = url_queue.pop(0)
            r = requests.get(test)

            data = r.text
            soup = BeautifulSoup(data, "html.parser")


            for link in soup.find_all('a'):
                link_str = str(link.get('href'))
                print(link_str)

                if counter > 15:
                    badWebsites.append(starter_website)

                if any(word in link_str.lower() for word in wordsToCheck):
                    if link_str.startswith('/url?q='):
                        link_str = link_str[7:]
                        # print('MOD:', link_str)
                    if '&' in link_str:
                        i = link_str.find('&')
                        link_str = link_str[:i]
                    if link_str.startswith('http') and not any(word in link_str.lower() for word in badWebsites):
                        f.write(link_str + '\n')
                        url_queue.append(str(link_str))
                        counter += 1
                        if starter_website not in link_str:
                            other_websites_count += 1


# function to determine if an element is visible
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

def cleanText(text):
    text = text.replace('\n', '')
    text = re.sub(' +', ' ', text)
    
    return text

def scrapeText(file):
    counter = 0
    urls = open(file, 'r')
    for line in urls:
        html = urllib.request.urlopen(line)
        soup = BeautifulSoup(html, "html.parser")
        data = soup.findAll(text=True)
        result = filter(visible, data)
        temp_list = list(result)
        temp_str = ' '.join(temp_list)

        temp_file_name = 'in/in' + str(counter) + '.txt'
        temp_file = open(temp_file_name, 'w')
        in_text = cleanText(temp_str)
        temp_file.write(in_text)

        out_file_name = 'out/out' + str(counter) + '.txt'
        out_file = open(out_file_name, 'w')

        in_tokens = sent_tokenize(in_text)
        for token in in_tokens:
            temp_sent = token + '\n'
            out_file.write(temp_sent)

        counter += 1

def emptyFolders():
    directoryIn = 'in'
    directoryOut = 'out'

def main():
    starter_url = "https://www.loudersound.com/features/the-making-of-pink-floyds-dark-side-of-the-moon"
    url_file = 'url.txt'

    webCrawler(starter_url, url_file)
    scrapeText(url_file)


if __name__ == '__main__':
    main()