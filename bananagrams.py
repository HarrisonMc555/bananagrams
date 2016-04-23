#!/use/bin/python3

def read_words():
    with open('words.txt') as fh:
        return fh.read().lower().split()

def word_frequencies(words):
    frequencies = {}
    for word in words:
        if word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 0
    return frequencies

def sort_word(word):
    return ''.join(sorted(word))

def whole_dict(frequencies):
    my_dict = {}
    for word in frequencies.keys():
        d = sort_word(word)
        if d in my_dict:
            my_dict[d].add(word)
        else:
            my_dict[d] = set([word])
    for k, v in my_dict.items():
        my_dict[k] = sorted(list(v),
                            key = lambda x: frequencies[x],
                            reverse=True)
    return my_dict

def test():
    return whole_dict(word_frequencies(read_words()))

def solver():
    input('Letters: ')

if __name__ == '__main__':
    solver()
