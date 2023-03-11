# Linus Fackler - LXF210001
# CS4395.001
# Dr. Mazidi
#
# Portfolio: Finding or Building a Corpus
#
# This program implements a web crawler that extracts information from websites based on a starting website, compiles information about important words and builds a knowledge base.
# This knowledge base can later be used to create a chatbot.
#

import requests
from bs4 import BeautifulSoup
import re
import urllib.request
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import math
import pickle

num_docs = 20           # number of websites to be used later

def webCrawler(starter_url, url_file):
    wordsToCheck = ['pink', 'floyd']        # words to check if URL is relevant
    badWebsites = ['google', 'facebook', 'twitter', 'pinterest', 'flipboard', 'shop']
    # words in websites to skip. These would produce bad results

    starter_website = 'loudersound'         # name of starter website, so program tries to find other websites
    other_websites_count = 0                # count of other websites found, different from starter website

    counter = 0                     # counter of total websites found
    url_queue = []                  # queue of all urls inspected
    url_queue.append(starter_url)

    with open(url_file, 'w') as f:
        while other_websites_count < 5:     # won't end until 5 other domains found (15 can be same as starter website)
            test = url_queue.pop(0)
            r = requests.get(test)          # pull website from queue

            data = r.text
            soup = BeautifulSoup(data, "html.parser")       # parse website


            for link in soup.find_all('a'):                 # check website
                link_str = str(link.get('href'))            # website to be checked
                print(link_str)

                if counter >= (num_docs - 5):               # if 15 websites of original domain reached, add starter domain to bad websites
                    badWebsites.append(starter_website)

                if any(word in link_str.lower() for word in wordsToCheck):
                    if link_str.startswith('/url?q='):      # clean url
                        link_str = link_str[7:]
                        # print('MOD:', link_str)
                    if '&' in link_str:                     # clean url
                        i = link_str.find('&')
                        link_str = link_str[:i]
                    
                    # good url found, write to urls.txt
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

# clean text, remove newlines and tabs/excessive spaces
def cleanText(text):
    text = text.replace('\n', '')
    text = re.sub(' +', ' ', text)
    
    return text

# scrape text from all 20 urls
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

        # print pretokened text to in file
        out_file_name = 'in/in' + str(counter) + '.txt'
        out_file = open(out_file_name, 'w')
        in_text = cleanText(out_str)
        
        text_list.append(in_text)

        out_file.write(in_text)

        out_file_name = 'out/out' + str(counter) + '.txt'
        out_file = open(out_file_name, 'w')

        # print cleaned & tokened text to out file
        in_tokens = sent_tokenize(in_text)
        for token in in_tokens:
            temp_sent = token + '\n'
            out_file.write(temp_sent)

        counter += 1
    return text_list

# create texdt frequency dictionary
def create_tf_dict(text):
    text = text.lower()             # lowercase text
    text = text.replace('\n', ' ')  # replace newlines

    # remove stopwords
    stopword = stopwords.words('english')
    tokens = word_tokenize(text)
    tokens = [w for w in tokens if w.isalpha() and w not in stopword]

    # term frequency tf
    token_set = set(tokens)
    tf_dict = {t:tokens.count(t) for t in token_set}

    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / len(tokens)

    return tf_dict

# create idf dictionary based on tf dictionaries
def create_idf_dict(vocab, tf_dicts):
    idf_dict = {}
    for term in vocab:
        temp = ['x' for voc in tf_dicts if term in voc.keys()]
        idf_dict[term] = math.log10((1 + num_docs) / (1 + len(temp)))
        # idf = log(N / (d∈D & t∈d))
        # N = number of documents; d = one document; D = set of documents
    return idf_dict

# create tf-idf
def create_tfidf(tf, idf):
    tf_idf = {}
    for t in tf.keys():
        tf_idf[t] = tf[t] * idf[t]
        # multiplying tf for each term in document by idf of term in corpus

    return tf_idf

# merge 2 dictionaries together
def mergeDictionaries(dict1, dict2):
    new_dict = {**dict1, **dict2}
    for key, value in new_dict.items():
        if key in dict1 and key in dict2:
            new_dict[key] = max(value, dict1[key])
            # if same word exists in both dictionaries, keep bigger score
        if len(key) < 3:
            new_dict[key] = 0
            # if word is less than 3 characters, delete it (set score to 0)

    return new_dict

def buildKnowledgeBase():
    # top 10 manually picked terms:
    # wembley, play, culture, edition, led zeppelin, abbey road, remastered, brain damage, waters, anniversary

    # sample sentences:
    text = "Hi, I'm Syd, a user-created fan-bot of psychedelic/progressive rock band Pink Floyd. What's your name? Hi <name>, do you like Pink Floyd? Awesome, me too. What's your favorite song? Mine is Brain Damage. That's sad to hear. Have you listened to their Album 'The Dark Side of the Moon' yet? It had its 50th anniversary this year. That's a good song. If you like Pink Floyd, you should play other albums like Led Zeppelin II or Abbey Road. You should give it a try! You can find the remastered edition on spotify. This album has influenced culture a lot."

    sents = sent_tokenize(text)
    return sents
    
def main():
    # starter website
    starter_url = "https://www.loudersound.com/features/the-making-of-pink-floyds-dark-side-of-the-moon"
    url_file = 'urls.txt'

    # find 20 urls
    webCrawler(starter_url, url_file)

    # scrape each url
    text_list = scrapeText(url_file)

    # create tf dictionary for each url
    tf_dicts = []
    for text in text_list:
        tf_dicts.append(create_tf_dict(text))

    # create total vocab
    vocab = set(tf_dicts[0].keys())
    for dic in tf_dicts[1:]:
        vocab = vocab.union(set(dic.keys()))

    print("number of unique words:", len(vocab))

    # create idf dictionary
    idf_dict = create_idf_dict(vocab, tf_dicts)

    # tf-idf
    tf_idfs = []
    for tf in tf_dicts:
        tf_idfs.append(create_tfidf(tf, idf_dict))

    # tf-idf for each text
    combined_tfidfs = tf_idfs[0]
    for t in tf_idfs[1:]:
        combined_tfidfs = mergeDictionaries(combined_tfidfs, t)

    # sort tf-idfs by score
    weights = sorted(combined_tfidfs.items(), key=lambda x:x[1], reverse=True)

    # print 40 most important words
    print("\n40 most important words in all texts:")
    for w in weights[:50]:
        # make output look readable first
        temp = str(w)
        temp = temp.replace('(', '')
        temp = temp.replace(')', '')
        temp = temp.replace(',', '')
        t = temp.split()
        print('{:>20}'.format(t[0]), '\t', t[1])

    # build knowledge base first
    knowledgeBase = buildKnowledgeBase()

    # create pickle from knowledge base
    pickle.dump(knowledgeBase, open('knowledgeBase.p', 'wb'))
    

if __name__ == '__main__':
    main()