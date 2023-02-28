import sys

def get_guess(data, target):
    return data[0]

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
    for word in data:
        word = check_word(word, pattern_dict, guess, correct)

        if (word is not None) and (word != guess):
            compatible.append(word)

    return compatible


def check_word(word, pattern_dict, guess, correct):
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
        guess = get_guess(data, target)

        pattern = get_pattern(guess, target)

        if (guess == target): return

        data = filter_data(data, pattern, guess)

        print(data, guess, pattern, target)



if __name__ == '__main__':
    if(len(sys.argv) != 3):
        print("Incorrect number of arguments. Input: python wordlesolver.py [word file] [target word]")

    filename, target = sys.argv[1], sys.argv[2]

    #define text file to open
    my_file = open(filename, 'r')

    #read text file into list
    data = my_file.read().split('\n')

    solve_wordle(data, target)
