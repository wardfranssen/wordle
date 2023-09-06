from bs4 import BeautifulSoup
import os
import random
import requests
import signal
import sys
import time


def what_is_daily_word():
    response = requests.get("https://docs.google.com/document/d/e/2PACX-1vSM3EGzJP-hcDNGgW0xonlEaAe368tNEfSUbiA5hpL"
                            "92M7WifGrjlU_CYofV1srq8tmghDnVXW-7LCu/pub")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract text content from the HTML
        text_content = " ".join([p.get_text() for p in soup.find_all('p')])
        return text_content
    else:
        print("Failed to fetch Google Doc. Status code:", response.status_code)
        print("\n try again or message ward.python@gmail.com")
        return None


def choose_random_word():
    try:
        with open("answers.txt") as wordList:
            word_list = wordList.read().splitlines()
            return random.choice(word_list)
    except FileNotFoundError:
        print("Couldn't find answers.txt make sure you have it in the same directory as this script.")
        sys.exit(0)


def word_is_real(guess_):
    try:
        is_real_word = False
        with open("words.txt") as wordlist:
            if wordlist.read().find(guess_) != -1:
                is_real_word = True
            return is_real_word
    except FileNotFoundError:
        print("Couldn't find words.txt make sure you have it in the same directory as this script.")
        sys.exit(0)


timer_start = 0
timer_finish = 0
guesses = 0


def incorrect():
    output = ["a", "a", "a", "a", "a"]
    letters_had = ""
    delete_last_line()
    for i in range(min(len(guess), 5)):
        if double_letters_guess() and not double_letters_word():
            if guess[i] == word[i]:
                output[i] = "\u001b[32m" + guess[i]  # green
                letters_had += guess[i]
    for i in range(min(len(guess), 5)):
        if guess[i] in word and guess[i] != word[i]:
            if guess[i] in letters_had:
                output[i] = "\u001b[37m" + guess[i]  # white
                letters_had += guess[i]
            else:
                output[i] = "\u001b[33m" + guess[i]  # yellow
                letters_had += guess[i]
        elif guess[i] == word[i]:
            output[i] = "\u001b[32m" + guess[i]  # green
            letters_had += guess[i]
        else:
            output[i] = "\u001b[37m" + guess[i]  # white
            letters_had += guess[i]
    print("".join(output))
    print("\u001b[37m")  # white
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
    elif guesses > 0:
        guess = input("Wrong, try again\n")

    if guesses < 1 and type_ == "inf":
        word = choose_random_word()
    elif guesses < 1 and type_ == "daily":
        word = what_is_daily_word()
    if len(guess) == 5 and word_is_real(guess):
        guesses += 1
        if guess.lower() == word.lower():
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
    return timer_finished_ - timer_start_


def double_letters_guess():
    not_duplicate_char = []
    duplicate_char_guess = []
    for i in range(min(len(guess), 5)):
        if guess[i] not in not_duplicate_char:
            not_duplicate_char.append(guess[i])
        else:
            duplicate_char_guess.append(guess[i])
    return duplicate_char_guess


def double_letters_word():
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
    if type_ == "inf" or type_ == "daily":
        wordle()
    else:
        print("Type either 'inf' or 'daily' so lets restart!")
        time.sleep(2)
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
    print("\nThe word was " + word)

    time.sleep(3)
    os.system("cls")
    sys.exit(0)


# if ctrl+c gets pressed call function signal_handler
signal.signal(signal.SIGINT, signal_handler)
# start the game
what_type()
