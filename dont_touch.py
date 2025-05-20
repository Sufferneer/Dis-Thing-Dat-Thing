# OUTDATED FORMAT
import json
alias = open('wordlist.txt', 'r').read().split('\n')
lejson = open('wordlist.json', 'w')
impString = {}
for i in range(0, len(alias) - 3, 4):
    impString[alias[i].split('||')[0]] = {
        "alias": alias[i].split('||')[1:len(alias[i].split('||'))],
        "translation": alias[i + 1].split('||'),
        "word_class": alias[i + 2],
        "definition": alias[i + 3]
    }
json_object = json.dumps(impString, indent = 4)
lejson.write(json_object)