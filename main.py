import time
from colored import fg
import random
import os
import signal
import sys


def choose_random_word():
    with open("words.txt") as wordList:
        word_list = wordList.read().splitlines()
        return random.choice(word_list)


def word_is_real(guess):
    isrealword = False
    with open("words.txt") as wordlist:
        if wordlist.read().find(guess) != -1:
            isrealword = True
    return isrealword


word = choose_random_word()
print("Lets play wordle!")
print("Guess a 5 letter word.")


def incorrect():
    print("incorrect, try again")

    output = ["a", "a", "a", "a", "a"]
    letters_had = ""

    for i in range(min(len(guess), 5)):
        if check_double_letters_guess() and not check_double_letters_word():
            if guess[i] == word[i]:
                output[i] = fg("green") + guess[i]
                letters_had += guess[i]

    for i in range(min(len(guess), 5)):
        if guess[i] in word and guess[i] != word[i]:
            if guess[i] in letters_had:
                output[i] = fg("white") + guess[i]
                letters_had += guess[i]
            else:
                output[i] = fg("yellow") + guess[i]
                letters_had += guess[i]
        elif guess[i] == word[i]:
            output[i] = fg("green") + guess[i]
            letters_had += guess[i]
        else:
            output[i] = fg("white") + guess[i]
            letters_had += guess[i]
    print("".join(output))
    print(fg("white"))
    letters_had = ""
    wordle()


def wordle():
    global guess
    guess = input("")

    if len(guess) == 5 and word_is_real(guess):
        if guess.lower() == word:
            print("Correct!")
            os.system("cls")
        else:
            incorrect()
    else:
        print("Must be a real 5 letter english word")
        wordle()


def check_double_letters_guess():
    not_duplicate_char = []
    duplicate_char_guess = []
    for i in range(min(len(guess), 5)):
        if guess[i] not in not_duplicate_char:
            not_duplicate_char.append(guess[i])
        else:
            duplicate_char_guess.append(guess[i])
    return duplicate_char_guess


def check_double_letters_word():
    not_duplicate_char_word = []
    duplicate_char_word = []
    for i in range(min(len(word), 5)):
        if word[i] not in not_duplicate_char_word:
            not_duplicate_char_word.append(word[i])
        else:
            duplicate_char_word.append(word[i])
    return duplicate_char_word


def signal_handler(sig, frame):
    print("\nYou pressed Ctrl+C!")
    print(word)
    time.sleep(2)
    os.system("cls")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
wordle()
