import requests, random
from mnemonic import Mnemonic

# word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

# response = requests.get(word_site)
# WORDS = response.content.splitlines()
# print (WORDS)



mnemo = Mnemonic("english")

words = mnemo.generate(strength=128)
print ('_'.join(random.sample(list(words.split()), 3)))
seed = mnemo.to_seed(words, passphrase="")
entropy = mnemo.to_entropy(words)
