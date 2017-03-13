import sys
import re

"""
Write a Python script that takes a Scrabble rack as a command-line argument and prints 
all valid Scrabble words that can be constructed from that rack, along with their 
Scrabble scores, sorted by score. An example invocation and output:

$ python scrabble.py ZAEFIEE
17 feeze
17 feaze
16 faze
15 fiz
15 fez
12 zee
12 zea
11 za
6 fie
6 fee
6 fae
5 if
5 fe
5 fa
5 ef
2 ee
2 ea
2 ai
2 ae
"""

"""
Compares the sorted rack with the sorted hash and returns the matches
"""
def get_rack_words(rack, hash):
    # if the string is empty, return an empty list
    if rack == '':
        return []
    
    # convert rack to regular expression, sorting the letters
    # and making each of them optional:
    rack = '^' + '?'.join(sorted(rack)) + '?$'
    
    # match with hashes (sorted letters) of dictionary words
    matches = re.findall(rack, '\n'.join(hash.keys()), re.IGNORECASE|re.MULTILINE)
    
    # convert hashes back to words
    words = []
    for match in matches:
        words += hash[match]
    return words 


"""    
Create a "hash" for each word: its letters are sorted
e.g. hash['back'] = 'adck'
"""
def key_dictionary(dictionary):
    hash = {}
    for word in dictionary.split('\n'):
        if re.match(r'\w+', word):
            key = ''.join(sorted(word))
            if (not key in hash):
                hash[key] = []
            hash[key].append(word)
    return hash

"""
Scores the words that match and returns a dictionary
"""
def score(matches):
  
  scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
         "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
         "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
         "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
         "x": 8, "z": 10}    
  
  hash_scores = dict.fromkeys(matches, 0)
  
  for key in hash_scores.keys():
    for char in key:
      hash_scores[key] += scores[char.lower()]
  
  return hash_scores

def main():

  """
  Get the Scrabble rack (the letters available to make words) from the 
  command line argument passed to your script.
  
  Handles the case where a a user forgets to supply a rack; in this case, print an error 
  message saying they need to supply some letters, and then exit the program using the 
  exit() function.
  """
  
  args = sys.argv[1:]
  if not args: 
    print 'Usage: scrabble.py [RACK]'
    sys.exit(1)
  # ensure it's a string 
  rack = str(args[0])
  
  """
  The code to open and read the sowpods word file. Create a list, where each 
  element is a word in the sowpods word file.
  """
  f = open('sowpods.txt', 'rU')
  dictionary = f.read()
  f.close()
  
  """
  The code to find all words from the word list that are made of letters that are a
  subset of the rack letters.
  """
  sorted_hash = key_dictionary(dictionary)
  matches = get_rack_words(rack, sorted_hash)
   
  """
  The code to determine the Scrabble scores for each valid word, using the scores
  dictionary from above.
  """
  scores = score(matches)

  for word in sorted(scores, key=scores.get, reverse=True):
    print "%d,%s" % (scores[word],word)
    
  return scores

if __name__ == '__main__':
  main()
