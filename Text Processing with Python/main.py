# Linus Fackler - LXF210001
# CS4395.001
# Dr. Mazidi
#
# This program reads in an employee list from a csv file. The path for which is passed in as sysarg.
# It then processes the input and prints out the list in a user-friendly format.
#

import sys
import os
import re
import pickle

class Person:
    def __init__ (self, last, first, mi, id, phone):
        self.last = last        # employee's last name
        self.first = first      # employee's first name
        self.mi = mi            # employee's middle initial
        self.id = id            # employee's ID
        self.phone = phone      # employee's phone number

    # this functions prints out the employee's information
    def display(self):
        print("Employee", end=" ")
        print("id:", self.id)
        print("\t", self.first, self.mi, self.last)
        print("\t", self.phone)

# this function checks if an entered employee ID is of a correct format (AB1234)
# if it's not, it will ask the user to enter a new ID
def check_id(id):
    pattern = re.compile(r"[A-Za-z][A-Za-z]\d{4}")
    while not pattern.match(id):
        print("ID invalid:", id)
        print("ID is two letters followed by 4 digits")
        print("Please enter a valid id:")
        id = input()
    
    # capitalize first 2 letters
    id = id[0].capitalize() + id[1].capitalize() + id[2:]
    return id

# this function checks if an entered phone number is of correct format (123-456-7890)
# if it's not, it will format it correctly
def check_phone(phone):
    if len(phone) != 10:                    # if not length 10, replace all wrong characters with a '-'
        return re.sub("[^0-9]", "-", phone)
    else:                                   # if length 10, insert '-' at correct positions
        return phone[:3] + '-' + phone[3:6] + '-' + phone[6:]

def process_input(file):
    
    # create persons dictionary
    persons = dict()
    
    # skip first line
    next(file)

    # iterate through all other lines in file
    for line in file:
        # split line at each ','
        words = line.split(",")

        last = words[0].capitalize()
        first = words[1].capitalize()
        mi = words[2].capitalize() if words[2] != "" else "X"   # if middle initial exists, capitalize it, otherwise "X"
        id = check_id(words[3])                                 # check if ID is correct format
        phone = check_phone(words[4].replace("\n", ""))         # check if phone number is correct format

        new_person = Person(last, first, mi, id, phone)         # create new Person with information

        # if ID exists already, don't create new person in dictionary
        if id in persons:
            print("ID already exists. Could not add user", id)
        else:
            persons[id] = new_person        # create new person in dictionary

    return persons          # return new dictionary
        

def main():

    # if system arguments are less than 2
    if len(sys.argv) < 2:
        print('Please enter a filename as a system argument')
        print("Exiting now...")
        sys.exit()      # exit program

    else:
        filepath = sys.argv[1]
        input = open(os.path.join(os.getcwd(), filepath), 'r')
        # this ensures that path is cross-platform

        persons = process_input(input)      # create new dictionary
        input.close()                       # close input file

        # save dictionary as pickle
        pickle.dump(persons, open('dict.p','wb'))

        # open pickle for read
        persons_output = pickle.load(open('dict.p', 'rb'))

        print("Employee list:\n")

        # print each person using Person display
        for employee in persons_output:
            persons_output[employee].display()

if __name__ == '__main__':
    main()  # call main function