import json
import string

for alpha in string.ascii_lowercase:
    try:
        f = open(f'words_unicode/{alpha}.json', 'r')
        content = json.load(f)
        w = open(f'words/{alpha}.json', 'w')
        w.write(json.dumps(content, indent = 4))
    except FileNotFoundError:
        print('does not exist')