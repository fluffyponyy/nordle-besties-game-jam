
import random 

secret_word = "teeny"
word_length = 5 #constant, only being used for clarity in case you don't know wordle

guesses = open("word_lists/wordle-guesses.txt").read().split('\n')
candidates = open("word_lists/wordle-candidates.txt").read().split('\n')

def isValidWord(word):
    length = len(word) 
    if length > word_length:
        return False

    if word not in candidates:
        if word not in guesses:
            return False
    
    return True

def toStrKey(str):
    key = ""
    for x in str:
        key += x
    return key

def toScore(list):
    score = 0
    score += list[0] * 1 #each green is worth one score points
    score += list[1] #each yellow is worth one score point
    return score

def computeBuckets(guess, word_list): #also should insert into hierarchy of buckets as it goes
    buckets = {}

    for word in word_list:
        result = compareWords(word, guess)
        key = toStrKey(result[0]) #turn the list of green/yellow/greys into one string eg bbygy
        bucket_score = toScore(result[1])
        
        #REDUNDANT; should simplify here
        if bucket_score in buckets.keys():
            if key in buckets[bucket_score].keys():
                buckets[bucket_score][key].append(word)
            else:
                buckets[bucket_score][key] = [word] 
        else:
            buckets[bucket_score] = {key: [word]} 
    return buckets

def getIndexes(word, letter):
    indexes = []
    for i in range(word_length):
        if word[i] == letter:
            indexes.append(i)
    return indexes

def compareWords(secret, guess):
    '''Returns a list with 5 elements; each element represents the color match between the two words
    'g' or green represents a letter in the correct place
    'y' or yellow represents a letter that is in the secret word but a different place
    'b' or black (grey in original) represents a letter that is not in the secret word'''
    pattern = [0, 0, 0, 0, 0]
    counts = [0, 0, 0] # # of greens, yellows, greys in that order
    greens = []
    yellows = []
    greys = []

    for i in range(word_length): #check for greens first
        if secret[i] == guess[i]:
            pattern[i] = "g"
            greens.append(i)
            counts[0] += 1
        else:
            greys.append(i)
    for i in greys:
        allIndexes = getIndexes(secret, guess[i])
        if len(allIndexes) != 0:
            for index in allIndexes:
                    if index not in greens and index not in yellows:
                        pattern[i] = "y"
                        counts[1] += 1
                        yellows.append(index)
                    else:
                        pattern[i] = "b"
        else:
                pattern[i] = "b"
                counts[2] += 1
    return pattern, counts


def getPattern(guess, remaining_candidates):
    if isValidWord(guess):
        buckets = computeBuckets(guess, remaining_candidates)
        minKey = sorted(buckets.keys())[0]
        minBuckets = buckets[minKey]
        remaining_keys = sorted(minBuckets.keys())
        if len(minBuckets) == 1: #if only one possible bucket remains
            remaining_candidates = minBuckets[remaining_keys[0]]
        else:
            remaining_candidates = minBuckets[remaining_keys[random.randint(0, (len(minBuckets))-1)]]

        print(remaining_candidates)
        pattern = compareWords(remaining_candidates[0], guess)[0]
        return pattern, remaining_candidates
    else:
        return -1

def getMessage(won, lost):
    playing_messsages = ["Oof.", "Unlucky.", "Try again.", "You suck at this.", "Mid.", "Cringe.", "Get good.", "I hate that.", "You need to try harder.", "Wrong.", "Supes wrong.", "Bad guess.", "Pathetic.", "Bad.", "Incorrect.", "Foul attempt.", "Bad one innit.", "Again."]
    if won:
        return "Finally. Press 'enter' to play again. "
    elif lost:
        return "Unforch. Press 'enter' to retry. "
    else:
        return playing_messsages[random.randint(0, len(playing_messsages)-1)]



# while True:

#     guess = input("word guess:")
#     guess = guess.lower()
#     if isValidWord(guess):
        
#         buckets = computeBuckets(guess, remaining_candidates)
#         minKey = sorted(buckets.keys())[0]
#         minBuckets = buckets[minKey]
#         remaining_keys = sorted(minBuckets.keys())
#         if len(minBuckets) == 1: #if only one possible bucket remains
#             remaining_candidates = minBuckets[remaining_keys[0]]
#         else:
#             remaining_candidates = minBuckets[remaining_keys[random.randint(0, len(minBuckets))]]
#         #next: place buckets in hierarchy and select highest from hierarchy, if only bucket is green then stop
#         print(remaining_candidates)
#         pattern = compareWords(remaining_candidates[0], guess)[0]
#         print(pattern)
#     else:
#         print("Enter a valid word.")
