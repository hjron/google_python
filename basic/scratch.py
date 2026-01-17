words = {}
f = open('list1.py', 'rt')

for line in f:
    for word in line.lower().split():
        if word in words:
            words[word] += 1
        else:
            words[word] = 1
            
for key in sorted(words.keys()):
# for k: v in sorted(words.items(), key=lambda x: x[1]):
    print(key, words[key])
