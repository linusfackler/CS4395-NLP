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

import requests
from bs4 import BeautifulSoup
import re
import urllib.request
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import math

num_docs = 20

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

                if counter >= (num_docs - 5):
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

    text_list = []

    for line in urls:
        html = urllib.request.urlopen(line)
        soup = BeautifulSoup(html, "html.parser")
        data = soup.findAll(text=True)
        result = filter(visible, data)
        temp_list = list(result)
        out_str = ' '.join(temp_list)

        out_file_name = 'in/in' + str(counter) + '.txt'
        out_file = open(out_file_name, 'w')
        in_text = cleanText(out_str)
        
        text_list.append(in_text)

        out_file.write(in_text)

        out_file_name = 'out/out' + str(counter) + '.txt'
        out_file = open(out_file_name, 'w')

        in_tokens = sent_tokenize(in_text)
        for token in in_tokens:
            temp_sent = token + '\n'
            out_file.write(temp_sent)

        counter += 1
    return text_list

def create_tf_dict(text):
    text = text.lower()
    text = text.replace('\n', ' ')

    stopword = stopwords.words('english')
    tokens = word_tokenize(text)
    tokens = [w for w in tokens if w.isalpha() and w not in stopword]

    # term frequency tf
    token_set = set(tokens)
    tf_dict = {t:tokens.count(t) for t in token_set}

    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / len(tokens)

    return tf_dict

def create_idf_dict(vocab, tf_dicts):
    idf_dict = {}
    for term in vocab:
        temp = ['x' for voc in tf_dicts if term in voc.keys()]
        idf_dict[term] = math.log10((1 + num_docs) / (1 + len(temp)))
    return idf_dict

def create_tfidf(tf, idf):
    tf_idf = {}
    for t in tf.keys():
        tf_idf[t] = tf[t] * idf[t]

    return tf_idf

def main():
    starter_url = "https://www.loudersound.com/features/the-making-of-pink-floyds-dark-side-of-the-moon"
    url_file = 'urls.txt'

    # -------------------------- remove comment later ----------------------------
    #webCrawler(starter_url, url_file)
    text_list = scrapeText(url_file)

    tf_dicts = []
    for text in text_list:
        tf_dicts.append(create_tf_dict(text))

    vocab = set(tf_dicts[0].keys())
    for dic in tf_dicts[1:]:
        vocab = vocab.union(set(dic.keys()))

    print("number of unique words:", len(vocab))

    # idf
    idf_dict = create_idf_dict(vocab, tf_dicts)

    # tf-idf
    tf_idfs = []
    for tf in tf_dicts:
        tf_idfs.append(create_tfidf(tf, idf_dict))

    # tf-idf for each text
    # combined_tfidfs = tf_idfs[0]
    # for t in tf_idfs[1:]:
    #     combined_tfidfs = combined_tfidfs | t

    # print(combined_tfidfs)

    # weights = sorted(combined_tfidfs.items(), key=lambda x:x[1], reverse=True)
    # print(weights)
    # # print("25 most important words in all texts:", weights[:25])


    i = 0
    for t in tf_idfs:
        weights = sorted(t.items(), key=lambda x:x[1], reverse=True)
        print("most important word in text ", i, ':', weights[:5])
        i += 1

if __name__ == '__main__':
    main()