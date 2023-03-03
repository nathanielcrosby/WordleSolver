import sys
import numpy as np
import time

def get_guess(data):
    curr = time.time()
    minguess = (None, 100000)

    # O(|W| * O(find_alpha))
    count = 0
    for g in data:
        count += 1
        alpha = find_alpha(g, data)
        #print(alpha)
        if (alpha < minguess[1]):
            minguess = (g, alpha)

    print(time.time() - curr)
    print(count)

    return minguess[0]


def find_alpha(g, data):
    total = 0
    patterns = {}

    #O(t) + 243*O(filter_data)
    #count = 0
    for t in data:
        if (t != g):
            pattern = get_pattern(g, t)
            if (patterns.get(tuple(pattern)) == None):
                #count += 1
                W = filter_data(data, pattern, g)
                #print(W, t, g)
                patterns[tuple(pattern)] = np.log(len(W))
                total += np.log(len(W))
            else:
                total += patterns.get(tuple(pattern))

    #print(count)

    return total


def get_pattern(guess, target):
    pattern = []
    correct = ''
    for i, ch in enumerate(guess):
        if (ch == target[i]):
            pattern.append('G')
            correct += ch
        elif (ch not in target):
            pattern.append('B')
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
    #print(data)
    for word in data:
        word = check_word(word, pattern_dict, guess, correct)

        if (word is not None) and (word != guess):
            compatible.append(word)

    return compatible


def check_word(word, pattern_dict, guess, correct):
    #print(pattern_dict, guess, word)
    for i in pattern_dict['B']:
        if ((guess[i] not in correct) and (guess[i] in word)) or ((word.count(guess[i]) > correct.count(guess[i])) and (guess.count(guess[i]) > correct.count(guess[i]))):
            return None
    for i in pattern_dict['G']:
        if guess[i] != word[i]:
            return None
    for i in pattern_dict['Y']:
        if ((correct.count(guess[i]) < word.count(guess[i])) and (guess.count(guess[i]) > correct.count(guess[i]))) or (correct.count(guess[i]) > word.count(guess[i])):
            return None

    return word


def solve_wordle(data, target):
    while(True):
        guess = get_guess(data)

        pattern = get_pattern(guess, target)

        if (guess == target): 
            print(guess)
            return

        data = filter_data(data, pattern, guess)

        print(guess, "".join(pattern))



if __name__ == '__main__':
    if(len(sys.argv) != 3):
        print("Incorrect number of arguments. Input: python wordlesolver.py [word file] [target word]")

    filename, target = sys.argv[1], sys.argv[2]

    #define text file to open
    my_file = open(filename, 'r')

    #read text file into list
    data = my_file.read().split('\n')

    solve_wordle(data, target)
