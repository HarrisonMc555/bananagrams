#!/usr/bin/python

import copy

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        if self.x < other.x:
            return True
        elif self.x > other.x:
            return False
        elif self.y < other.y:
            return True
        elif self.y > other.y:
            return False
        else:
            return False

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return 37 * self.x + 89 * self.y

class PointRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def left_right(self):
        return self.start.y == self.end.y

    def __iter__(self):
        if self.left_right():
            for x in range(self.start.x, self.end.x):
                yield Point(x, self.start.y)
        else:
            for y in range(self.start.y, self.end.y):
                yield Point(self.start.x, y)

class Board:
    def __init__(self):
        self.words = {}
        self.grid = {}

    def __getitem__(self, point):
        return self.grid[point]

    def add_word(self, word, point, left_right):
        result = copy.deepcopy(self)
        if left_right:
            end = Point(point.x + len(word),  point.y)
        else:
            end = Point(point.x,  point.y + len(word))
        point_range = PointRange(point, end)
        result.words[point_range] = word
        for i, point in enumerate(point_range):
            result.grid[point] = word[i]
        return result

    def __str__(self):
        min_x = min(self.grid.keys(), key = lambda p: p.x).x
        max_x = max(self.grid.keys(), key = lambda p: p.x).x
        min_y = min(self.grid.keys(), key = lambda p: p.y).y
        max_y = max(self.grid.keys(), key = lambda p: p.y).y
        real_grid = [[None] * (max_x - min_x + 1)
                     for i in range(min_y, max_y + 1)]
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                point = Point(x, y)
                i = y - min_y
                j = x - min_x
                if point in self.grid:
                    real_grid[i][j] = self.grid[point]
                else:
                    real_grid[i][j] = ' '
        return '\n'.join([''.join(row) for row in real_grid])

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

def add_word(coords, bag, board):
    must_use = board[coords]


def start_game():
    board = {}


def test():
    return whole_dict(word_frequencies(read_words()))

def solver():
    input('Letters: ')

if __name__ == '__main__':
    print(Board()
          .add_word('kthxbai', Point(5,6), True)
          .add_word('karp', Point(5,6), False)
          .add_word('karp', Point(10,5), False))
