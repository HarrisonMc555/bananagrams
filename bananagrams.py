#!/usr/bin/env python3

import copy


LEFT_RIGHT = True
UP_DOWN = False


class BanagramsException(Exception):
    pass


class Point:
    """A cartesian coordinate"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def left(self, off=1):
        """Returns a point to the left of self."""
        return Point(self.x-off, self.y)

    def right(self, off=1):
        """Returns a point to the right of self."""
        return Point(self.x+off, self.y)

    def up(self, off=1):
        """Returns a point to the up of self."""
        return Point(self.x, self.y-off)

    def down(self, off=1):
        """Returns a point to the down of self."""
        return Point(self.x, self.y+off)

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

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __repr__(self):
        return 'Point({}, {})'.format(self.x, self.y)


class PointRange:
    """A range of cartesian coordinates"""
    def __init__(self, start, end):
        if start.x != end.x and start.y != end.y:
            # raise Exception("{} and {} are not in same row or column".format(
            raise BanagramsException("{} and {} are not in same row or column".
                                     format(start, end))
        self.start = start
        self.end = end

    def left_right(self):
        """True if horizontal

        True if horizontal (left->right)
        False if vertical (top->bottom)

        """
        return self.start.y == self.end.y

    def __iter__(self):
        """Returns each point in the range"""
        if self.left_right():
            for x in range(self.start.x, self.end.x):
                yield Point(x, self.start.y)
        else:
            for y in range(self.start.y, self.end.y):
                yield Point(self.start.x, y)

    def __contains__(self, point):
        """Return True if a point is in the range"""
        if self.left_right():
            return point.y == self.start.y and \
                self.start.x <= point.x <= self.end.x
        else:
            return point.x == self.start.x and \
                self.start.y <= point.y <= self.end.y

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return 211*hash(self.start) + 223*hash(self.end)

    def __str__(self):
        return '[{}..{}]'.format(self.start, self.end)

    def __repr__(self):
        return 'PointRange({}, {})'.format(repr(self.start), repr(self.end))


class Board:
    """A board of letter tiles

    words (PointRange->str)
      Dictionary that maps a PointRange to the word found in that range

    grid (Point->char)
      A dictionary that maps a Point to the character found at that point

    connections (PointRange->[PointRange])
      A list of all of the words that a given word is connected to. The
      PointRange of each word is used as a unique identifier

    """
    def __init__(self):
        self.words = {}
        self.grid = {}
        self.connections = {}

    def __getitem__(self, point):
        return self.grid[point]

    def add_first_word(self, word):
        return self.add_word(word, Point(0, 0), LEFT_RIGHT)
        # # print('add_first_word: <{}>'.format(word))
        # result = copy.deepcopy(self)
        # point = Point(0, 0)
        # # default to left-right for first word
        # end = Point(point.x + len(word),  point.y)
        # point_range = PointRange(point, end)
        # result.words[point_range] = word
        # result.connections[point_range] = []
        # for i, point in enumerate(point_range):
        #     result.grid[point] = word[i]
        # # print('add_first_word:', result)
        # return result

    def add_word(self, word, point, left_right):
        """Returns a new board with the added word

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
        result.connections[point_range] = []
        for i, point in enumerate(point_range):
            if point in result.grid and result.grid[point] != word[i]:
                raise BanagramsException("Word didn't overlap correctly")
            result.grid[point] = word[i]
            connected_words = [pr for pr in self.words if point in pr]
            result.connections[point_range].extend(connected_words)
            for connected_word in connected_words:
                result.connections[connected_word].append(point_range)
        return result

    def remove_word(self, point_range):
        connected_words = self.connections[point_range]
        if any([len(self.connections[pr]) <= 1 for pr in connected_words]):
            raise BanagramsException("Deleting this word would divide board" +
                                     "into separte boards")
        result = copy.deepcopy(self)
        del result.connections[point_range]
        del result.words[point_range]
        for point in point_range:
            # only delete points that weren't in any of the connections
            if not [point for pr in connected_words if point in pr]:
                del result.grid[point]
        return result

    def __str__(self):
        if not self.grid:
            return ""
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


def read_words(filename):
    """Reads words from text file"""
    with open(filename) as fh:
        return fh.read().lower().split()


def word_frequencies(words):
    """Returns dictionary of words->frequencies

    words ([str])       : array of words
    return ({str : int}) : dictionary of words->frequencies

    """
    frequencies = {}
    for word in words:
        if word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 1
    return frequencies


def sort_word(word):
    """Returns a sorted version of the word"""
    return ''.join(sorted(word))


def whole_dict(frequencies):
    """Returns a dictionary of letter sets->list of words sorted by frequency

    Each key in the dictionary is a string of letters in alphabetical order.
    Each value in the dictionary is a list of words that contain exactly the
    same letters as their respective keys.  The words are in order from most
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


def presorted_dict(words):
    my_dict = {}
    for word in words:
        k = sort_word(word)
        if k in my_dict:
            my_dict[k].append(word)
        else:
            my_dict[k] = [word]
    return my_dict


def add_word(bag, board, my_dict):
    """Add one word to the board using given letters."""
    if not board.grid:
        words = get_longest_word(bag, my_dict)
        if not words:
            raise BanagramsException(
                "Coudln't find a word containing letters", bag)
        word = words[0]
        new_board = board.add_first_word(word)
        remaining_letters = subtract_word(bag, word)
        # print('remaining_letters({}, {}) = "{}"'.format(bag, word,
        #                                                 remaining_letters))
        return new_board, remaining_letters
    # print('add letters:', bag)
    for letters in all_substrings(bag):
        # print('Try with these letters: "{}"'.format(letters))
        for point in board.grid:
            for new_board in try_to_add_word(point, letters, board, my_dict):
                # Stop trying, use first viable option
                remaining_letters = subtract_word(bag, letters)
                # print('about to leave add_word.\n',
                #       '\tboard: {}\n\tremaining: {}'.format(repr(new_board),
                #                                             remaining_letters))
                return new_board, remaining_letters
        # for point, char in board.grid.items():
        #     print("\tHere: {} '[{}]'".format(point, char))
        #     all_letters = letters + char
        #     # for word in my_dict[sort_word(all_letters)]:
        #     code = sort_word(all_letters)
        #     if code not in my_dict:
        #         print('\tno words found containing letters "{}"'.format(
        #             code))
        #         continue
        #     words = my_dict[code]
        #     for word in words:
        #         print('\t\tword: {}'.format(word))
        #         for origin, direction in places_to_add_word(point,
        #                                                     word, board):
        #             # Stop trying, use first viable option
        #             print('\t\tPlacing {} at {} (left-to-right? {})'.format(
        #                 word, origin, direction))
        #             return board.add_word(word, origin, direction)
    return board, bag


def try_to_add_word(point, letters, board, my_dict):
    """Uses the letters in the bag to place a word on the board

    The `coords` is a Point that the word will intersect on the board. A word
    will be chosen that is comprised of this letter and additional letters
    taken from the bag. The word will be placed on the board.

    The word that is placed will not intersect with any other words that were
    previously placed on the board.

    point (Point)   : the point of intersection on the board
    bag (set(char)) : the available letters to use
    board (Board)   : the board to place the word on

    """
    char = board[point]
    # print("\tTry here: {} '[{}]'".format(point, char))
    all_letters = letters + char
    code = sort_word(all_letters)
    if code not in my_dict:
        # print('\tno words found containing letters "{}"'.format(
        #     code))
        return
    words = my_dict[code]
    for word in words:
        # print('\t\tword: {}'.format(word))
        for origin, direction in places_to_add_word(point, word, board):
            # print('\t\tPlacing {} at {} (left-to-right? {})'.format(
            #     word, origin, direction))
            yield board.add_word(word, origin, direction)


def places_to_add_word(point, word, board):
    """Yields (Point, direction) possibilities of placing word on board.

    Yields the possible ways possible to add `word` to `board` such that
    `char` overlaps the `board` at `point`.

    """
    char = board.grid[point]
    # print("\t\tTry here: {} '{}'".format(point, char))
    # There can't be anything in either direction of the direction we're
    # trying our purposes. We could theoretically add something to the right
    # if it could extend the previous word or to the left if it could prepend
    # it but we're not going to worry about that right now.

    # Try left & right
    if point.left() not in board.grid and point.right() not in board.grid:
        # print('\t\t\tTry left-to-right')
        for i in findOccurences(word, char):
            # print('\t\t\t\tfound {} at position {} in {}'.format(
            #     char, i, word))
            origin = point.left(i)
            points = PointRange(origin, origin.right(len(word)))
            for i, p in enumerate(points):
                # print('\t\t\t\t\ti = {}, p = {}:'.format(i, p))
                if (p in board.grid and board.grid[p] != word[i]) or \
                   (p != point and (p.up() in board.grid or
                                    p.down() in board.grid)):
                    # print('\t\t\t\t\tFound problem....')
                    break
            else:
                # print("\t\t\tDidn't find conflicts along or next to line")
                left_end = origin.left()
                right_end = origin.right(len(word))
                if left_end not in board.grid and right_end not in board.grid:
                    yield (origin, LEFT_RIGHT)

    # Try up & down
    if point.up() not in board.grid and point.down() not in board.grid:
        # print('\t\t\tTry up-to-down with:', word, char)
        # print(board)
        for i in findOccurences(word, char):
            # print('i: {} ({}[{}] = {})'.format(i, word, i, char))
            origin = point.up(i)
            points = PointRange(origin, origin.down(len(word)))
            for c, p in zip(word, points):
                # print('i: {}, p: {}'.format(i, p))
                # print('grid:', board.grid)
                # print(p, 'p         in board.grid:', p in board.grid)
                # print(p, 'p.left()  in board.grid:', p.left() in board.grid)
                # print(p, 'p.right() in board.grid:', p.right() in board.grid)
                # print('p == origin:', p == origin)
                if (p in board.grid and board.grid[p] != word[i]) or \
                   (p != point and (p.left() in board.grid or
                                    p.right() in board.grid)):
                    break
            else:
                up_end = origin.up()
                down_end = origin.down(len(word))
                if up_end not in board.grid and down_end not in board.grid:
                    yield (origin, UP_DOWN)


def remove_letters(string, n):
    """ Yield all combinations of removing n letters from the string """
    if n <= 0 or not string:
        yield string
    else:
        for i in range(len(string)):
            yield from remove_letters(string[:i]+string[i+1:], n-1)


def all_substrings(string):
    for i in range(len(string)):
        yield from remove_letters(string, i)


def get_longest_word(letters, my_dict):
    """ Get the longest word that uses only the given letters

    Iterates through using all the letters, then all minus one, etc. until it
    finds a word that uses all of those letters (and only those letters).

    """
    for word in all_substrings(letters):
        # print(word)
        code = sort_word(word)
        if code in my_dict:
            return my_dict[code]
    else:
        return None


def subtract_word(string, sub):
    """ Removes the given substring from the string """
    # print('subtract_word:', string, sub)
    for c in sub:
        if c not in string:
            # what to do here?
            pass
        string = string.replace(c, '', 1)
    # print('\tstring:', string)
    return string


def start_game(letters):
    global board
    board = {}  # board = Board()


def create_dict():
    """Creates a dictionary of word sets to sorted words from file"""
    # return whole_dict(word_frequencies(read_words('words.txt')))
    return presorted_dict(read_words('common-non-proper.txt'))


def solver():
    input('Letters: ')


def findOccurences(s, ch):
    return (i for i, letter in enumerate(s) if letter == ch)


def interactive():
    print(welcome_msg())
    d = create_dict()
    b = Board()
    input_letters = parse_input(input())
    remaining, remaining_last = input_letters, None
    while input_letters:
        while remaining and remaining != remaining_last:
            # print('inner loop')
            # print('board: {}, remaining: {} ({})'.format(
            #     repr(b), remaining, type(remaining)))
            remaining_last = remaining
            b, remaining = add_word(remaining, b, d)
        if remaining:
            print(couldnt_place_msg(remaining))
        print('\nBoard:\n\n{}\n'.format(b))
        input_letters = parse_input(input())
        remaining, remaining_last = input_letters, None
    print(goodbye_msg())


def parse_input(input_string):
    return ''.join([s.lower() for s in input_string if s.isalpha()])


def welcome_msg():
    return """Welcome to the Bananagrams machine!

Enter one or more letters and press enter. The machine will figure out a good
place to put those letters.

Hit enter twice to quit.
"""


def goodbye_msg():
    return """Thanks for playing with the Bananagrams machine!"""


def couldnt_place_msg(remaining):
    return "Couldn't place these letters: {}".format(remaining)


def test():
    b = (Board()
         .add_word('kthxbai', Point(5, 6), LEFT_RIGHT)
         .add_word('karp', Point(5, 6), UP_DOWN)
         .add_word('karp', Point(10, 5), UP_DOWN))
    print(b)
    print()
    print(b.grid)
    print(b.words)
    p = Point(7, 6)
    print(list(places_to_add_word(p, 'hah', b)))
    p = Point(10, 8)
    print(list(places_to_add_word(p, 'paappp', b)))
    my_dict = create_dict()
    print(list(my_dict.items())[:10])
    for code, words in my_dict.items():
        if len(words) > 5:
            print(code, words[:15])
    if not b:
        exit()
    b2, remaining = add_word('ush', b, my_dict)
    print('b2')
    print()
    print(b2)
    print('\n'+'-'*20)
    if not b2:
        print('here')
        print(b)
        exit()
    print('past')
    b3, remaining = add_word('asd', b2, my_dict)
    print('b3:')
    print()
    print(b3)
    print('\n'+'-'*20)
    if not b3:
        print(b2)
        exit()

    # Dallin's try
    b4, remaining = add_word('dehanig', b3, my_dict)
    print('remaining:', remaining)
    print()
    print(b4)
    print('\n'+'-'*20)
    if not b4:
        print(b3)
        exit()
    if not remaining:
        exit()
    b5, remaining = add_word(remaining, b4, my_dict)
    print('remaining:', remaining)
    print()
    print(b5)
    print('\n'+'-'*20)
    if not b5:
        print(b4)
        exit()

    # another try
    b6, remaining = add_word('itrba', b5, my_dict)
    print('remaining:', remaining)
    print()
    print(b6)
    print('\n'+'-'*20)
    if not b6:
        print(b5)
        exit()
    if not remaining:
        exit()
    b7, remaining = add_word(remaining, b6, my_dict)
    print('remaining:', remaining)
    print()
    print(b7)
    print('\n'+'-'*20)
    if not b7:
        print(b6)
        exit()


def remove_test():
    b = Board().add_word("black", Point(0, 0), LEFT_RIGHT)
    print(b)
    print(b.connections)
    print()

    b = b.add_word("board", Point(0, 0), UP_DOWN)
    print(b)
    print(b.connections)
    print()

    b = b.add_word("ace", Point(0, 2), LEFT_RIGHT)
    print(b)
    print(b.connections)
    print()

    # b = b.remove_word(PointRange(Point(0, 0), Point(0, 5)))
    try:
        b = b.remove_word(PointRange(Point(0, 0), Point(0, 5)))
        raise Exception(
            "Shouldn't have been able to remove word that would split board")
    except BanagramsException:
        pass

    b = b.add_word("are", Point(2, 0), UP_DOWN)
    print(b)
    print(b.connections)
    print()

    b = b.remove_word(PointRange(Point(0, 0), Point(0, 5)))
    print(b)
    print(b.connections)
    print()


def main():
    remove_test()
    # interactive()


if __name__ == '__main__':
    main()
