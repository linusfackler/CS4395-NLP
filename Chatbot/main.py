# Linus Fackler - LXF210001
# CS4395.001
# Dr. Mazidi
#
# HLT – Chatbot Project
#
# This program creates a chatbot that can answer questions about bands, including what genre it is and what members are active.
# It gets the information by scraping from wikipedia pages.
#

import requests
from bs4 import BeautifulSoup
import spacy
from spacy.tokens import Span
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pickle

nlp = spacy.load("en_core_web_sm")      # trained pipeline for English
band_label = "BAND"
Span.set_extension("label_", default=None, force=True)

# some of the words that will guide the bot towards an answer
band_infos = ["genre", "origin", "where", "members", "since", "active"]

# return a response from the bot
def get_response(user_input, context):
    # Look for a band name in the user's input
    band_match = re.search(r"(?i)\b(band)\b\s+(\w+\s?)+", user_input)
    if band_match:
        band = band_match.group(0).replace("band", "").strip().replace(" ", "_")
        # Check if we already have information about this band
        if band.lower() in context.get("bands", {}):
            # Scrape the band's Wikipedia page for information
            url = f"https://en.wikipedia.org/wiki/{context['bands'][band.lower()]}"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            # Extract the band's description
            description = soup.select_one(".mw-parser-output p").get_text()
            context["current_band"] = band.lower()
            return f"{band.capitalize()} is a band that {description} What else would you like to know?", 1
        else:
            # Ask the user for information about the band
            context["current_band"] = band.lower()
            display_name = band.replace("_", " ").title()
            # return f"What would you like to know about {display_name}?\n", 0
            return f"I can tell you more about {display_name}! Do you like this band?\n", 0

    # If the user asks any basic information about the band
    elif any(inf in user_input.lower() for inf in band_infos) and context.get("current_band"):
        # Scrape the current band's Wikipedia page for the infobox
        url = f"https://en.wikipedia.org/wiki/{context['current_band']}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        infobox = soup.find("table", class_="infobox")

        display_name = context.get("current_band").replace("_", " ").title()

        if infobox:

            # genre
            if "genre" in user_input.lower():
                genres_row = infobox.find("th", string="Genres").parent

                # Extract the genres from the row
                genres = [genre.text for genre in genres_row.find_all("a")]

                if genres:
                    return f"{display_name} plays {genres[0]}.", 1
                else:
                    return f"I'm sorry, I couldn't find the genre for {display_name}.", 1

            
            # origin/where
            if "origin" in user_input.lower() or "where" in user_input.lower():
                origin_element = infobox.select_one('th:-soup-contains("Origin")')

                # Extract the genres from the row
                origin = origin_element.find_next_sibling("td").get_text().strip()

                if origin:
                    return f"{display_name} is from {origin}.", 1
                else:
                    return f"I'm sorry, I couldn't find the origin of {display_name}.", 1

            # members
            if "members" in user_input.lower():
                members_element = infobox.select_one('th:-soup-contains("Members")')
                
                if members_element is None:
                    members_element = infobox.select_one('th:-soup-contains("members")')


                members = members_element.find_next_sibling("td").get_text().strip()

                members = members.replace('\n', ', ')
                members = members.split(', ')
                if members:
                    if len(members) > 1:
                        mem = ", ".join(members[:-1]) + ", and " + members[-1]
                        return f"{display_name}'s current/latest members are {mem}.", 1
                    else:
                        return f"{display_name} currently consists of {members[0]}.", 1
                else:
                    return f"I'm sorry, I couldn't find the members of {display_name}.", 1

            # since/active
            if "since" in user_input.lower() or "active" in user_input.lower():
                years_active_element = infobox.select_one('th:-soup-contains("Years active")')
                if years_active_element:
                    years_active = years_active_element.find_next_sibling("td").get_text().strip()
                    # Clean up the text
                    years_active = re.sub(r"\[.*?\]", "", years_active)
                    years_active = re.sub(r"\s+", " ", years_active)

                    act = re.split('–| ', years_active)
                    if "present" in years_active:
                        return f"{display_name} has been active since {act[0]}.", 1
                    else:
                        return f"{display_name} was active from {act[0]} to {act[-1]}.", 1
                else:
                    return f"I'm sorry, I couldn't find the active years of {display_name}.", 1

        # if we can't find the requested information
        return f"I'm sorry, I couldn't find the information you requested for {display_name}.", 1
    

    # if we're currently looking for information about a band, save the user's input and return a response
    elif context.get("current_band"):
        # Scrape the current band's Wikipedia page for the requested information
        url = f"https://en.wikipedia.org/wiki/{context['bands'][context['current_band']]}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        # Extract the requested information
        section = soup.select_one(f"#{context['current_band']}_")
        if section:
            return section.get_text(), 1
        else:
            return "I'm sorry, I couldn't find that information.", 1
    # if we don't understand the user's input, respond with a default message
    return "I'm sorry, I didn't understand you.", 1

# get user's name
def get_name(input):
    doc = nlp(input)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "there"       # in case name is not recognized

# check if user likes or dislikes a band
def get_like(input):
    # Initialize the sentiment analyzer
    sid = SentimentIntensityAnalyzer()
    
    # Get the polarity scores for the response
    scores = sid.polarity_scores(input)
    
    # Determine if the sentiment is positive or negative based on the compound score
    if scores['compound'] > 0.05:
        return 'like'
    elif scores['compound'] < -0.05:
        return 'dislike'
    else:
        return 'neutral'

# main function to run the chat bot
def main():
    print("Syd: Hi! I'm Syd! A user-created chat-bot that can answer questions about famous bands in music history!")
    print("Syd: What's your name?\n")

    name_input = input("You: ")
    
    user_name = get_name(name_input)

    try:        # if user already has a previous conversation
        user_data = pickle.load(open(f'pickles/{user_name}.p', 'rb'))
    except:     # if no old conversation with username found
        user_data = {}

    print(f"\nSyd: Hi {user_name}! What questions do you have for me?\n")

    user_data["name"] = user_name

    context = {"bands": {}}

    while True:
        user_input = input("You: ")
        print()
        if user_input.lower() == "exit" or user_input.lower() == "quit":
            print("Syd: Nice talking to you!")
            pickle.dump(user_data, open(f'pickles/{user_name}.p','wb'))        # pickle user data

            break   # exit
        else:
            bot_response, response_index = get_response(user_input, context)
            if context.get("current_band"):
                # If the user asked for information about a band, save it to the context
                context["bands"][context["current_band"]] = bot_response
            print("Syd:", bot_response)

            # this is for the first response per band
            if (response_index == 0):
                like_response = input("You: ")
                display_name = context["current_band"].replace("_", " ").title()
                like_result = get_like(like_response)
                user_data[context["current_band"]] = like_result

                if (like_result == "like"):
                    print(f"\nSyd: That's good to hear! What do you want to know about {display_name}?\n")
                elif (like_result == "dislike"):
                    print(f"\nSyd: It's not everyone's taste! What do you want to know about {display_name}?\n")
                else:
                    print(f"\nSyd: Interesting! What do you want to know about {display_name}?\n")

            # any other response
            else:
                print("Syd: Anything else you want to know?\n")


if __name__ == "__main__":
    main()