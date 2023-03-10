import sys
import numpy as np
from termcolor import colored


def get_guess(data):
    """ Calculates alpha for each possible guess and returns the (guess, alpha) tuple with the lowest alpha. """

    minguess = (None, float("inf"))

    for g in data:
        alpha = find_alpha(g, data)

        if (alpha < minguess[1]):
            minguess = (g, alpha)

    return minguess


def find_alpha(g, data):
    """ For a potential guess g, calculate the number of target words that generate each pattern, then calculate alpha for the guess overall. """
    
    patterns = {}

    for t in data:
        if (t != g):
            pattern = tuple(get_pattern(g, t))
            if (patterns.get(pattern) != None):
                patterns[pattern] += 1 
            else:
                patterns[pattern] = 1

    total = 0
    for p in patterns.keys():
        total += patterns[p] * np.log(patterns[p])

    return total


def get_pattern(guess, target):
    """ Return a list of 'G', 'Y', and 'B' representing the wordle pattern for a guess and target. """

    pattern = []
    correct = ''
    for i, ch in enumerate(guess):
        if (ch == target[i]):
            pattern.append('G')
            correct += ch
        else:
            pattern.append('?')

    for i, val in enumerate(pattern):
        if val == '?':
            if (correct.count(guess[i]) < target.count(guess[i])):
                pattern[i] = 'Y'
                correct += guess[i]
            else:
                pattern[i] = 'B'
    
    return pattern

def filter_data(data, pattern, guess):
    """ Return a list of words that filters out all words incompatible with a given guess and pattern. """

    correct = ''
    pattern_dict = {'B':[], 'G':[], 'Y':[]}
    for i, val in enumerate(pattern):
        if (val != 'B'):
            correct += guess[i]
        pattern_dict[val].append(i)

    compatible = []
    for word in data:
        word = check_word(word, pattern_dict, guess, correct)

        if (word is not None) and (word != guess):
            compatible.append(word)

    return compatible


def check_word(word, pattern_dict, guess, correct):
    """ Helper function for filter_data that checks whether a word is compatible with the guess and pattern. """

    for i in pattern_dict['G']:
        if guess[i] != word[i]:
            return None
        
    for i in pattern_dict['Y']:
        if (word[i] == guess[i]):
            return None
        if ((correct.count(guess[i]) < word.count(guess[i])) and (guess.count(guess[i]) > correct.count(guess[i]))):
            return None
        if (correct.count(guess[i]) > word.count(guess[i])):
            return None
        
    for i in pattern_dict['B']:
        if (word[i] == guess[i]):
            return None
        if ((guess[i] not in correct) and (guess[i] in word)) or ((word.count(guess[i]) > correct.count(guess[i])) and (guess.count(guess[i]) > correct.count(guess[i]))):
            return None

    return word


def solve_wordle(data, target, compute_first):
    """ Main function that solves the wordle query given a set of words and a target. """

    if (not compute_first):
        guess, alpha = 'tares', 79277.23353563494
    else:
        guess, alpha = get_guess(data)

    pattern = get_pattern(guess, target)
    print("".join(get_colors(pattern, guess)), alpha)
    
    while(guess != target):
        data = filter_data(data, pattern, guess)

        guess, alpha = get_guess(data)

        pattern = get_pattern(guess, target)

        print("".join(get_colors(pattern, guess)), alpha)


def get_colors(pattern, guess):
    """ Helper function to color the outputted text to show the pattern over the guessed word. """

    colored_pattern = []
    for i, letter in enumerate(pattern):
        if letter == 'G':
            colored_pattern.append(colored(guess[i], 'blue', on_color='on_green'))
        elif letter == 'Y':
            colored_pattern.append(colored(guess[i], 'blue', on_color='on_yellow'))
        else:
            colored_pattern.append(colored(guess[i], 'white'))

    return colored_pattern


if __name__ == '__main__':
    if(len(sys.argv) < 3):
        print("Incorrect number of arguments. Input: python wordlesolver.py word_file target_word [--compute-first-guess] [-c]")

    else:
        filename, target = sys.argv[1], sys.argv[2]

        #define text file to open
        try:
            my_file = open(filename, 'r')
        except FileNotFoundError:
            print("No file found with name: ", filename)
            print("Ensure the correct arguments. Input: python wordlesolver.py word_file target_word [--compute-first-guess] [-c]")

        #read text file into list
        data = my_file.read().split('\n')

        compute_first = False
        if (len(sys.argv) > 3) and ((sys.argv[3] == '--compute-first-guess') or (sys.argv[3] == '-c')): 
            compute_first = True
        elif (len(sys.argv) > 3):
            print("Unrecognized argument found: ", sys.argv[3])
            print("Ensure the correct arguments. Input: python wordlesolver.py word_file target_word [--compute-first-guess] [-c]")
            sys.exit()


        if (target in data):
            solve_wordle(data, target, compute_first)

        else:
            print(f"The word {target} was not found in the file {filename}. Retry with a correct word from the list.")
