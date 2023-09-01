from colored import fg
import os
import random
import signal
import sys
import time

global guess
global word
global type_
prev_guess_yellow = []
prev_guess_green = []


def what_is_daily_word():
    with open("dailyword.txt") as dailywordtxt:
        daily_word = dailywordtxt.read()
        dailywordtxt.close()
    return daily_word


def choose_random_word():
    with open("answers.txt") as wordList:
        word_list = wordList.read().splitlines()
        return random.choice(word_list)


def word_is_real(guess_):
    is_real_word = False
    with open("words.txt") as wordlist:
        if wordlist.read().find(guess_) != -1:
            is_real_word = True
        return is_real_word


timer_start = 0
timer_finish = 0
guesses = 0


def hardmode(guess_):
    global guess
    global prev_guess_yellow
    global prev_guess_green
    global place_green
    print(prev_guess_green)
    for i in range(len(place_green)):
        if prev_guess_green[place_green[i]] != guess[i]:
            print("Green must be in the same place")
            wordle()
    for i in range(len(prev_guess_yellow)):
        if prev_guess_yellow[i] not in guess:
            print("Yellow must be in your new guess")
            wordle()


def incorrect():
    global guess
    global prev_guess_yellow
    global prev_guess_green
    global place_green
    place_green = []
    prev_guesses = []
    output = ["a", "a", "a", "a", "a"]
    letters_had = ""
    delete_last_line()
    prev_guesses.append(guess)
    if type_ == "hard" and guesses > 1:
        print(guess)
        hardmode(guess)
    for i in range(min(len(guess), 5)):
        if check_double_letters_guess() and not check_double_letters_word():
            if guess[i] == word[i]:
                output[i] = fg("green") + guess[i]
                letters_had += guess[i]
                prev_guess_green.append(guess[i])

    for i in range(min(len(guess), 5)):
        if guess[i] in word and guess[i] != word[i]:
            if guess[i] in letters_had:
                output[i] = fg("white") + guess[i]
                letters_had += guess[i]
            else:
                output[i] = fg("yellow") + guess[i]
                letters_had += guess[i]
                prev_guess_yellow.append(guess[i])
        elif guess[i] == word[i]:
            output[i] = fg("green") + guess[i]
            letters_had += guess[i]
            prev_guess_green.append(guess[i])
            place_green.append(i)
        else:
            output[i] = fg("white") + guess[i]
            letters_had += guess[i]
    print(prev_guess_yellow)
    print("".join(output))
    print(fg("white"))
    wordle()


def wordle():
    global guess
    global guesses
    global timer_start
    global timer_finish
    global word
    global type_
    game_finished = False
    if guesses == 0:
        guess = input("Type a 5 letter word\n")
        prev_guess = guess
    elif guesses > 0:
        prev_guess = guess
        guess = input("Wrong, try again\n")

    if type_ == "inf" or type_ == "hard" and guesses == 0:
        word = choose_random_word()
    elif type_ == "daily":
        word = what_is_daily_word()
    if len(guess) == 5 and word_is_real(guess):
        guesses += 1
        if guess.lower() == word:
            if guesses == 1:
                print("Correct!")
                print("You got it first try, lucky bastard!")
                print("It took you 0 seconds")
                game_finished = True
            else:
                timer_finish = time.time()
                os.system("cls")
                rounded_time = str(round(total_time(timer_finish, timer_start), 2))
                game_finished = True
                print("Took you " + rounded_time + " seconds and " + str(guesses) + " guesses to get it!")

        else:
            if guesses == 1:
                timer_start = time.time()
                incorrect()
            elif not game_finished:
                incorrect()

    else:
        print("Must be a real 5 letter english word")
        wordle()


def total_time(timer_finished_, timer_start_):
    return timer_finished_-timer_start_


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


def what_type():
    global type_
    print("Lets play wordle!")
    type_ = input("Do you want play the daily wordle(daily) or the infinite version(inf)\n")
    type_ = type_.lower()
    if type_ == "inf" or type_ == "daily" or type_ == "hard":
        wordle()
    else:
        print("Type either 'inf' or 'daily' so lets restart!")
        time.sleep(10)
        os.system("cls")
        what_type()


def delete_last_line():
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K\n')


def signal_handler(sig, frame):
    global timer_finish
    global timer_start

    timer_finish = time.time()
    rounded_time = str(round(total_time(timer_finish, timer_start), 2))
    if timer_start == 0:
        print("You have not guessed any word and already gave up!")
    else:
        print("Took you " + rounded_time + " seconds and " + str(guesses) + " guesses to give up!")
    # print("\nYou pressed ctrl+c")
    print("\nThe word was " + word)

    time.sleep(3)
    os.system("cls")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

what_type()
