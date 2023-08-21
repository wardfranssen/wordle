import datetime
import random
import os
import time

with open("dailywords.txt") as wordlists:
    word_list = wordlists.read().splitlines()
    daily_word = random.choice(word_list)

with open("dailywords.txt", "r") as wordlistss:
    content = wordlistss.read()

with open("dailywords.txt", "w") as wordlistss:
    wordlistss.write(content.replace(daily_word, ""))

with open("Already_had_daily.txt", "a") as wordlist:
    wordlist.write(daily_word + "\n")
    wordlist.close()

open('.dailyword.txt', 'w').close()
with open(".dailyword.txt", "a") as dailywordtxt:
    dailywordtxt.write(daily_word)
    dailywordtxt.close()

os.system("shutdown /s /t 1")
