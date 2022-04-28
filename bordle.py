#!/usr/bin/env python3
######################################################################
#
# Copyright 2022 Bryan Murdock
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see
# <https://www.gnu.org/licenses/>.
#
######################################################################
import argparse
import random
import sys

WORDS='/usr/share/dict/words'

# shamelessly taken from: https://stackoverflow.com/a/61960902/27729
def colored(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text}\033[38;2;255;255;255m"


def red(text):
    return colored(255, 0, 0, text)


def green(text):
    return colored(0, 255, 0, text)


def yellow(text):
    return colored(255, 255, 0, text)


class Keyboard:
    def __init__(self):
        self.keyboard = [['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', ],
                         ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ],
                         ['z', 'x', 'c', 'v', 'b', 'n', 'm', ]]

    def color_key(self, color, letter):
        for key_row in self.keyboard:
            for i, key in enumerate(key_row):
                # the or is because a yellow letter could turn green:
                if letter == key or letter == yellow(key):
                    key_row[i] = color(key)

    def print(self):
        for i, key_row in enumerate(self.keyboard):
            if i == 1:
                print(' ', end='')
            if i == 2:
                print('  ', end='')
            for key in key_row:
                print(f' {key} ', end='')
            print()


class Bordle:
    def __init__(self, length, max_guesses, word):
        print("correct letter, wrong place: -X-")
        print("correct letter, correct place: *X*")
        self.words = []
        self.the_word = ''
        self.guesses = []
        self.keyboard = Keyboard()
        self.num_guesses = 0
        self.word_length = 5
        self.max_guesses = self.word_length + 1
        if length:
            self.word_length = length
            if max_guesses:
                self.max_guesses = max_guesses
            else:
                self.max_guesses = self.word_length + 1

        if not word:
            with open(WORDS) as words_file:
                for word in words_file:
                    word = word.rstrip()
                    if len(word) == self.word_length \
                       and not word[0].isupper() \
                       and "'" not in word:
                        self.words.append(word)
            assert len(self.words)
            self.the_word = random.choice(self.words)
        else:
            self.the_word = word
        if len(self.the_word) != self.word_length:
            print(f'ERROR: chosen word, {self.the_word} is not '
                  f'{self.word_length} letters long')
            sys.exit(1)
        for i in range(self.max_guesses):
            guess = ''
            for j in range(self.word_length):
                guess += ' '
            self.guesses.append(guess)

    # TODO: be more helpful with the hints, like wordle is, I think.
    # For example, if you guess a word with repeating letters, and you
    # have the repeated letter in the correct space and in a wrong
    # space, don't indicate that the letter is correct but in the
    # wrong place.
    #
    # lets say the word is trips if you guess title, currently this
    # code will show both t's as valid letters when it shouldn't
    #
    # I think I just need to temporarily remove the guesses letter
    # from the_word if it's found.  It might be nice to decouple this
    # from display_grid, but not now.
    def display_grid(self):
        for guess_id in range(self.max_guesses):
            temp_the_word = list(self.the_word)
            print('    ', end='')
            for letter_id in range(self.word_length):
                letter = self.guesses[guess_id][letter_id]
                if letter == temp_the_word[letter_id]:
                    print(f'| {green(letter)} ', end='')
                    temp_the_word[letter_id] = ' '
                    self.keyboard.color_key(green, letter)
                elif letter in temp_the_word:
                    print(f'| {yellow(letter)} ', end='')
                    self.keyboard.color_key(yellow, letter)
                else:
                    print(f'| {letter} ', end='')
                    self.keyboard.color_key(red, letter)
                if letter_id == self.word_length - 1:
                    print('|', end='')
            print()
        self.keyboard.print()

    def validate_guess(self, guess):
        if guess == 'giveup':
            print(f'YOU LOSE!  The word was {self.the_word}')
            sys.exit(1)
        if guess == 'reci mi':
            print(self.the_word)
        if len(guess) > self.word_length:
            print(f'{guess} is too long, try again')
        elif len(guess) < self.word_length:
            print(f'{guess} is too short, try again')
        elif guess not in self.words:
            print(f'{guess} is not in the word list, try again')
        else:
            return True
        return False

    def check_if_done(self):
        if self.num_guesses == self.max_guesses:
            print('Wah wah.  So close!')
            print(f'the word was: {self.the_word}')
            sys.exit(1)
        if self.guesses[self.num_guesses - 1] == self.the_word:
            print('Well done!')
            sys.exit(0)


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--word-length', type=int, action='store',
                        help='length of word, defaults to 5 letters')
    parser.add_argument('-g', '--max-guesses', type=int, action='store',
                        help='max number of guesses, defaults to '
                        'word-length plus 1')
    parser.add_argument('-w', '--word', type=str, action='store',
                        help=f'the secret word, default is a randomly chosen '
                        'word from {WORDS}')
    return parser.parse_args()


def main(args):
    bordle = Bordle(args.word_length, args.max_guesses, args.word)
    while True:
        bordle.display_grid()
        bordle.check_if_done()
        try:
            guess = input('guess a word: ')
        except KeyboardInterrupt:
            print('\nDone so soon?  Buh-bye')
            sys.exit(1)
        print('\n')
        if bordle.validate_guess(guess):
            bordle.guesses[bordle.num_guesses] = guess
            bordle.num_guesses += 1


if __name__ == '__main__':
    sys.exit(main(parse_args(sys.argv)))
