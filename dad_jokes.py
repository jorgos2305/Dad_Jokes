# This program get a random dad joke, just for fun
# It saves the jokes as a csv file
# So, it does not do anything useful, but gives me a chance to practice :)
# this is powered by https://icanhazdadjoke.com/api

import requests
import csv
import os
import json

headers = {'accept':'application/json'}

def get_joke(base_url='https://icanhazdadjoke.com/', headers=headers):
    """Return one random joke."""
    # According to the API documentation headers requesting JSON must be sent like this
    # No query params necessary for the random joke
    response = requests.get(base_url, headers=headers)
    return response.json()

def get_joke_by_theme(theme, base_url='https://icanhazdadjoke.com/search', query={'limit':30}, headers=headers):
    """Returns a joke of a specified theme, if no jokes found it returns None"""
    # A maximum of 30 jokes will be fetch from the API
    # The theme is sent as a query parameter, if you request a theme for which no jokes were found you will get an empty list of jokes
    query['term'] = theme
    response = requests.get(base_url, params=query, headers=headers)
    jokes_dict = response.json()
    if len(jokes_dict['results']) == 0:
        return None # No jokes found for the specified theme
    return jokes_dict

def user_input(input_message='Enter a word:'):
    """Returns a word entered by the user as a string."""
    correct_input = False
    while not correct_input:
        word = input(input_message)
        if not word.isalpha():
            print('All characters must be letters. Try again.')
        else:
            correct_input = True
    return word

def save_to_csv(dict_joke):
    """Takes a dictionary joke as input and stores the joke and its ID in a CSV file"""
    headers = ['ID', 'Joke'] # This is the data returned from the API
    file_exists = os.path.exists('jokes.csv') # Check if the file exists
    with open('jokes.csv', 'a') as jokes_list:
        writer = csv.writer(jokes_list)
        if not file_exists: # If the file does not exit place the headers, if it does continue to the next step
            writer.writerow(headers)
        writer.writerow([dict_joke['id'], dict_joke['joke']])
    return


def main():
    print('''
    Welcome to random dad jokes
    Wanna hear a joke?
    Tell me what you want to do

    (1) Tell me a random dad joke
    (2) Tell me a dad joke with some specific theme
    (0) I've had enough jokes for today, bye bye!
    ''')

    valid_selection = False
    # Normal listener loop
    while not valid_selection:
        selection = input('So? what do you want to do?\n')
        try:
            selection = int(selection)
            if selection >= 0 and selection <= 2: # Can be updated if program grows
                valid_selection = True
            else:
                print('\nMmmh there are only the two possibilities... Think again')
        except:
            print("\nC'mon! 1 or 2 o 0, how hard can that be!?")

    if selection == 0:
        exit()
    
    elif selection == 1:
        joke = get_joke()
        print(f"Today's joke is... \n{joke['joke']}\n")
        valid_selection = False
        while not valid_selection:
            save = input('Wanna save your joke to tell at parties? (y/n)\n').lower()
            if save == 'y':
                save_to_csv(joke)
                valid_selection = True
            elif save == 'n':
                valid_selection = True
            else:
                print('Please, enter only y = yes / n = no.') 

    elif selection == 2:
        theme = user_input('\nWhat do you want to hear a joke about?\n')
        # This is a dictionary with the results. The key 'results'  has as values a list of dictionary with the keys 'id' and 'joke' 
        jokes = get_joke_by_theme(theme) 
        if jokes is None:
            print(f'No jokes for {theme} were found. Sorry!')
        else:
            # joke is a dictionary with the keys 'id' and 'joke'
            print('I found {} jokes about {}. I will tell you all of them, prepare yourself!\nYou will have to decide for every joke if you want to save it :)'.format(jokes['total_jokes'], theme))
            for joke in jokes['results']:
                print('{}'.format(joke['joke']))
                print()
                valid_selection = False
                while not valid_selection:
                    save = input('Wanna save your joke to tell at parties? (y/n)\n').lower()
                    if save == 'y':
                        save_to_csv(joke) # This function recieves a dicionary as input and stores the joke into the file
                        valid_selection = True
                    elif save == 'n':
                        valid_selection = True
                    else:
                        print('Please, enter only y = yes / n = no.')


if __name__ == '__main__':
    finished = False
    while not finished:
        main()
        again = user_input('Woud you like to hear another joke?\n')
        if again == 'y':
            os.system('clear')
        elif again == 'n':
            finished = True
        else:
            print('Invalid selection. Good bye.')
            exit()
