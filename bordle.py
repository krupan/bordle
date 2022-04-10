#!/usr/bin/env python3
######################################################################
#
# edge cases:
# - guessed the word
# - guessed the word on last guess
# - failed to guess the word and ran out of guesses
# - guessed too short word
# - guessed too long word
# - guessed non-word
#
######################################################################
import argparse
import random
import sys

WORDS='/usr/share/dict/words'

class Keyboard:
    def __init__(self):
        self.keyboard = [['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', ],
                         ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ],
                         ['z', 'x', 'c', 'v', 'b', 'n', 'm', ]]

    def remove_key(self, letter):
        for key_row in self.keyboard:
            for i, key in enumerate(key_row):
                if letter == key:
                    key_row[i] =  '_'

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
    def __init__(self, length, max_guesses):
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

        with open(WORDS) as words_file:
            for word in words_file:
                word = word.rstrip()
                if len(word) == self.word_length \
                   and not word[0].isupper() \
                   and "'" not in word:
                    self.words.append(word)
        assert len(self.words)
        self.the_word = random.choice(self.words)
        assert len(self.the_word) == self.word_length
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
    def display_grid(self):
        for guess_id in range(self.max_guesses):
            print('    ', end='')
            for letter_id in range(self.word_length):
                letter = self.guesses[guess_id][letter_id]
                if letter == self.the_word[letter_id]:
                    print(f'|*{letter}*', end='')
                elif letter in self.the_word:
                    print(f'|-{letter}-', end='')
                else:
                    print(f'| {letter} ', end='')
                    self.keyboard.remove_key(letter)
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
    return parser.parse_args()


def main(args):
    bordle = Bordle(args.word_length, args.max_guesses)
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
