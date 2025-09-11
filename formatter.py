import json


def myFunc(e):
  return e[0].lower()
f = open('word.txt', 'r')
content = f.read().split('\n')
for i in range(len(content)):
    content[i] = content[i].split('||')
    content[i][2] = content[i][2].lower()
content.sort(key = myFunc)
curLetter = 'a'
curLetterPointer = 0
leEntryList = []
leList = []
ascii = 'abcdefghijklmnopqrstuvwxyz'
for entry in content:
    if entry[0][0].lower() == curLetter:
        leEntryList.append(
            {
                "word": entry[0],
                "plural": entry[1],
                "word_class": entry[2],
                "translation": entry[3],
                "definition": entry[4]
            }
        )
    else:
        curLetterPointer += (ord(entry[0][0].lower()) - ord(curLetter))
        overrideFile = open(f'assets/words/{curLetter}.json', 'w')
        overrideFile.write(json.dumps(leEntryList, ensure_ascii=False, indent=4))
        print(leEntryList)
        curLetter = ascii[curLetterPointer]
        leEntryList = []
        leEntryList.append(
            {
                "word": entry[0],
                "plural": entry[1],
                "word_class": entry[2],
                "translation": entry[3],
                "definition": entry[4]
            }
        )
overrideFile = open(f'assets/words/{curLetter}.json', 'w')
overrideFile.write(json.dumps(leEntryList, ensure_ascii=False, indent = 4))