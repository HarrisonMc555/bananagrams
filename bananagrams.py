#!/usr/bin/env python3

import copy


class Point:
    """ A cartesian coordinate """
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
    """ A range of cartesian coordinates """
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def left_right(self):
        """ True if horizontal

        True if horizontal (left->right)
        False if vertical (top->bottom)
        """
        return self.start.y == self.end.y

    def __iter__(self):
        """ Returns each point in the range """
        if self.left_right():
            for x in range(self.start.x, self.end.x):
                yield Point(x, self.start.y)
        else:
            for y in range(self.start.y, self.end.y):
                yield Point(self.start.x, y)


class Board:
    """ A board of letter tiles

    words (PointRange->str) : Dictionary that maps a PointRange to the word
                              found in that range
    grid (Point->char)      : A dictionary that maps a Point to the character
                              found at that point
    """
    def __init__(self):
        self.words = {}
        self.grid = {}

    def __getitem__(self, point):
        return self.grid[point]

    def add_word(self, word, point, left_right):
        """ Returns a new board with the added word

        word (str)        : word to add
        point (Point)     : origin of word
        left_right (bool) : going left->right or top->bottom
        """
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
        min_x = min(self.grid.keys(), key=lambda p: p.x).x
        max_x = max(self.grid.keys(), key=lambda p: p.x).x
        min_y = min(self.grid.keys(), key=lambda p: p.y).y
        max_y = max(self.grid.keys(), key=lambda p: p.y).y
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
    """ Reads words from text file """
    with open('words.txt') as fh:
        return fh.read().lower().split()


def word_frequencies(words):
    """ Returns dictionary of words->frequencies

    words ([str])       : array of words
    return ({str->int}) : dictionary of words->frequencies
    """
    frequencies = {}
    for word in words:
        if word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 0
    return frequencies


def sort_word(word):
    """ Returns a sorted version of the word """
    return ''.join(sorted(word))


def whole_dict(frequencies):
    """ Returns a dictionary of letter sets->list of words sorted by frequency

    Each key in the dictionary is a string of letters in alphabetical
    order. Each value in the dictionary is a list of words that contain exactly
    the same letters as their respective keys. The words are in order from most
    frequent to least frequent.
    """
    my_dict = {}
    for word in frequencies.keys():
        d = sort_word(word)
        if d in my_dict:
            my_dict[d].add(word)
        else:
            my_dict[d] = set([word])
    for k, v in my_dict.items():
        my_dict[k] = sorted(list(v),
                            key=lambda x: frequencies[x],
                            reverse=True)
    return my_dict


def add_word(coords, bag, board):
    """Uses the letters in the bag to place a word on the board

    The `coords` is a Point that the word will intersect on the board. A word
    will be chosen that is comprised of this letter and additional letters
    taken from the bag. The word will be placed on the board.

    The word that is placed will not intersect with any other words that were
    previously placed on the board.

    coords (Point)  : the point of intersection on the board
    bag (set(char)) : the available letters to use
    board (Board)   : the board to place the word on

    """
    must_use = board[coords]


def remove_letters(string, n):
    """ Yield all combinations of removing n letters from the string """
    if n == 0:
        yield string
    else:
        for i in range(len(string)):
            yield from remove_letters(string[:i]+string[i+1:], n-1)


def get_longest_word(letters, my_dict):
    """ Get the longest word that uses only the given letters

    Iterates through using all the letters, then all minus one, etc. until it
    finds a word that uses all of those letters (and only those letters).
    """
    for i in range(len(letters)):
        for word in remove_letters(letters, i):
            # print(word)
            code = sort_word(word)
            if code in my_dict:
                return my_dict[code]
    else:
        return None


def subtract_word(string, sub):
    """ Removes the given substring from the string """
    for c in sub:
        if c not in string:
            # what to do here?
            pass
        string = string.replace(c, '', 1)
    return string


def start_game(letters):
    board = {}  # board = Board()


def create_dict():
    """ Creates a dictionary of word sets to sorted words from file """
    return whole_dict(word_frequencies(read_words()))


def solver():
    input('Letters: ')


if __name__ == '__main__':
    print(Board()
          .add_word('kthxbai', Point(5, 6), True)
          .add_word('karp', Point(5, 6), False)
          .add_word('karp', Point(10, 5), False))
