import random
import os

# picks a random word from dailywords.txt
with open("dailywords.txt") as wordlists:
    word_list = wordlists.read().splitlines()
    daily_word = random.choice(word_list)
    word_list.close()


with open("dailywords.txt", "r") as dailywords:
    content = dailywords.read()
    dailywords.close()

with open("dailywords.txt", "w") as dailywords:
    dailywords.write(content.replace(daily_word, ""))

with open("Already_had_daily.txt", "a") as Already_had:
    Already_had.write(daily_word + "\n")
    Already_had.close()

open('dailyword.txt', 'w').close() # clears dailyword.txt
with open("dailyword.txt", "a") as dailyword:
    dailyword.write(daily_word)
    dailyword.close()

#os.system("shutdown /s /t 1")
