import random
import os

# picks a random word from dailywords.txt
with open("dailywords.txt") as dailywords:
    word_list = dailywords.read().splitlines()
    daily_word = random.choice(word_list)
    dailywords.close()

# reads the dailywords, so it can remove the new daily word
with open("dailywords.txt", "r") as dailywords:
    content = dailywords.read()
    dailywords.close()

# removes the daily word in the dailywords file
with open("dailywords.txt", "w") as dailywords:
    dailywords.write(content.replace(daily_word, ""))

# adds the new daily word to the file
with open("alreadyHadDaily.txt", "a") as alreadyHadDaily:
    alreadyHadDaily.write(daily_word + "\n")
    alreadyHadDaily.close()

 # clears dailyword.txt
open('dailyword.txt', 'w').close()

# writes the new daily word in the file
with open("dailyword.txt", "a") as dailyword:
    dailyword.write(daily_word)
    dailyword.close()

# os.system("shutdown /s /t 1")
