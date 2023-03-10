Wordle Solver by Nathaniel Crosby and David Dang

Running the Program:

python wordlesolver.py [word_file] [target_word] [--compute-first-guess] [-c]

the optional flag --compute-first-guess is the same as -c.
Normally, the first guess for the wordle solver is "tares" because for the full wordlewords.txt file, we have determined this to be optimal.
Enter this flag for a different list of words so that a optimal guess for that list can be found, or if you simply wish to let the program solve for the first guess again.

Warning: When the first guess is hardcoded, a solution is found in seconds, but when it is not, it takes a few minutes to compute an initial guess.


How we select our distribution when there are multiple words with the same alpha:
We simply select the word that we computed alpha for first which is whichever word appears first in the inputted list.
Since it doesn't matter what the distribution is, we went for the simplest choice to reduce complexity.