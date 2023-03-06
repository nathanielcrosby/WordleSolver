import sys
import numpy as np
import time
from termcolor import colored

def get_guess(data):
    curr = time.perf_counter()
    minguess = (None, float("inf"))
    timer = 0

    for g in data:
        alpha = find_alpha(g, data)

        if (alpha < minguess[1]):
            minguess = (g, alpha)

    print(time.perf_counter() - curr, timer)
    return minguess


def find_alpha(g, data):
    total = 0
    patterns = {}

    curr = time.perf_counter()
    for t in data:
        if (t != g):
            pattern = tuple(get_pattern(g, t))
            if (patterns.get(pattern) != None):
                patterns[pattern] += 1 
            else:
                patterns[pattern] = 1
    
    #print("1", time.perf_counter() - curr)
    curr = time.perf_counter()

    for p in patterns.keys():
        W = filter_data(data, p, g)
        total += patterns[p] * np.log(len(W))

    #print("2", time.perf_counter() - curr)

    return total


def get_pattern(guess, target):
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
    for i in pattern_dict['G']:
        if guess[i] != word[i]:
            return None
    for i in pattern_dict['Y']:
        if ((correct.count(guess[i]) < word.count(guess[i])) and (guess.count(guess[i]) > correct.count(guess[i]))) or (correct.count(guess[i]) > word.count(guess[i])):
            return None
    for i in pattern_dict['B']:
        if ((guess[i] not in correct) and (guess[i] in word)) or ((word.count(guess[i]) > correct.count(guess[i])) and (guess.count(guess[i]) > correct.count(guess[i]))):
            return None

    return word


def solve_wordle(data, target):
    while(True):
        guess, alpha = get_guess(data)

        pattern = get_pattern(guess, target)

        if (guess == target): 
            print("".join(get_colors(pattern, guess)), alpha)
            return

        data = filter_data(data, pattern, guess)

        print("".join(get_colors(pattern, guess)), alpha)


def get_colors(pattern, guess):
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
    if(len(sys.argv) != 3):
        print("Incorrect number of arguments. Input: python wordlesolver.py [word file] [target word]")

    else:
        filename, target = sys.argv[1], sys.argv[2]

        #define text file to open
        try:
            my_file = open(filename, 'r')
        except FileNotFoundError:
            print("No file found with name: ", filename)
            print("Ensure the correct arguments. Input: python wordlesolver.py [word file] [target word]")

        #read text file into list
        data = my_file.read().split('\n')

        if (target in data):
            solve_wordle(data, target)

        else:
            print(f"The word {target} was not found in the file {filename}. Retry with a correct word from the list.")
