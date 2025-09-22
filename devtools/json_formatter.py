import json

if input('You will accept that all word files will be overridden. (Y/N): ').lower() == 'y':
	def myFunc(e):
		return e[0].lower()
	f = open('word.csv', 'r')
	content = f.read().split(',"')
	for i in range(1, len(content)):
		content[i] = content[i].split(' ')
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
					"word": entry[0].replace('"', ''),
					"plural": entry[1].replace('"', ''),
					"class": entry[2].replace('"', ''),
					"translation": entry[3].replace('"', ''),
					"definition": entry[4].replace('"', '')
				}
			)
		else:
			curLetterPointer += (ord(entry[0][0].lower()) - ord(curLetter))
			overrideFile = open(f'assets/data/words/{curLetter}.json', 'w')
			overrideFile.write(json.dumps(leEntryList, ensure_ascii=False, indent=4))
			print(leEntryList)
			curLetter = ascii[curLetterPointer]
			leEntryList = []
			leEntryList.append(
				{
					"word": entry[0].replace('"', ''),
					"plural": entry[1].replace('"', ''),
					"class": entry[2].replace('"', ''),
					"translation": entry[3].replace('"', ''),
					"definition": entry[4].replace('"', '')
				}
			)
	overrideFile = open(f'assets/data/words/{curLetter}.json', 'w')
	overrideFile.write(json.dumps(leEntryList, ensure_ascii=False, indent = 4))
	print('All files overridden. Good luck lol')