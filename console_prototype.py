import json
import os
wordList = []
def binary_search_word(x):
    low = 0
    high = len(wordList) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if x in wordList[mid]['word']:
            return wordList[mid]
        elif wordList[mid]['word'][0] < x or len(wordList[mid]['word'][0]) > len(x):
            low = mid + 1
        else:
            high = mid - 1
    return None
def display_word(worddata):
    print(worddata['word'][0].upper())
    print(worddata['word_class'])
    if len(worddata['alt_spellings']) > 0:
        print('Acceptable Spellings: ' + ' | '.join(worddata['alt_spellings'][0:]))
    print(worddata['definition'])
while True:
    ins = input('Search for a word: ')
    if ins.isalpha() and os.path.exists(f'words/{ins[0]}.json'):
        wordFile = open(f'words/{ins[0]}.json', 'r')
        wordList = json.load(wordFile)
        wordFile.close()
        wordData = binary_search_word(ins)
        if wordData:
            display_word(wordData)