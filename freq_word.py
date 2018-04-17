word_counts = {}

with open('135013.txt') as fh:
    line = fh.readline()
    line = fh.readline()
    while line:
        comments = line.split('|')[1]
        print(comments)
        line = fh.readline()