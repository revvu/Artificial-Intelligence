import sys; args = sys.argv[1:]
# Reevu Adakroy, pd. 7
# started 4/16/2021
import re

oldDictionary = open('dictionary.txt', 'r').read().splitlines()
myDictionary = []
#remove words with caps
for word in oldDictionary:
    if word.lower()==word and re.fullmatch('[a-z]*',word):
        myDictionary+=[word]

def continuous_block_count(word):
    max_length = 0
    lst = [*word]
    current_char = lst[0]

    current_length = 1
    for i in range(len(word)-1):
        if lst[i+1]==current_char:
            current_length+=1
        else:
            current_char = lst[i+1]
            max_length = max(current_length, max_length)
            current_length = 1

    max_length = max(current_length, max_length)
    return max_length

def repeated_letter_count(word):
    max_count = 0
    letter_set = set()
    for letter in word:
        letter_set.add(letter)
    for letter in letter_set:
        max_count=max(max_count, word.count(letter))

    return max_count

def consonant_count(word):
    count = 0

    lst = [*word]
    for letter in lst:
        if letter not in 'aeiou':
            count+=1

    return count

def adjacent_count(word):
    max_count = 0
    count = 0
    lst = [*word]
    for i in range(len(lst)-1):
        if lst[i]==lst[i+1]:
            count+=1
            i+=1
        else:
            max_count = max(max_count, count)
            count = 0
    return max_count

longest_block_count = 0
repeated_letter = 0
consonant = 0
adjacent = 0

max_count_word = ''
for word in myDictionary:
    longest_block_count = max(longest_block_count, continuous_block_count(word))
    repeated_letter = max(repeated_letter_count(word), repeated_letter)
    consonant = max(consonant_count(word), consonant)
    if adjacent_count(word)>adjacent:
        adjacent =adjacent_count(word)
        max_count_word = word

print('Longest continuous block: ' + str(longest_block_count))
print('Most repeated letters: ' + str(repeated_letter))
print('Most consonants: ' + str(consonant))
print('Most adjacent pairs: ' + str(adjacent))
print(max_count_word)
