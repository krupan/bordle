#!/usr/bin/env python3
import random
import sys

WORDS='/usr/share/dict/words'
WORD_LENGTH = 5
MAX_GUESSES = 5

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
    def __init__(self):
        print("correct letter, wrong place: -X-")
        print("correct letter, correct place: *X*")
        self.words = []
        self.the_word = ''
        self.guesses = []
        self.num_guesses = 0
        self.keyboard = Keyboard()

        with open(WORDS) as words_file:
            for word in words_file:
                word = word.rstrip()
                if len(word) == WORD_LENGTH \
                   and not word[0].isupper() \
                   and "'" not in word:
                    self.words.append(word)
        assert len(self.words)
        self.the_word = random.choice(self.words)
        assert len(self.the_word) == WORD_LENGTH
        for i in range(MAX_GUESSES):
            guess = ''
            for j in range(WORD_LENGTH):
                guess += ' '
            self.guesses.append(guess)

    def display_grid(self):
        for guess_id in range(MAX_GUESSES):
            print('    ', end='')
            for letter_id in range(WORD_LENGTH):
                letter = self.guesses[guess_id][letter_id]
                if letter == self.the_word[letter_id]:
                    print(f'|*{letter}*', end='')
                elif letter in self.the_word:
                    print(f'|-{letter}-', end='')
                else:
                    print(f'| {letter} ', end='')
                    self.keyboard.remove_key(letter)
                if letter_id == WORD_LENGTH - 1:
                    print('|', end='')
            print()
        self.keyboard.print()

    def validate_guess(self, guess):
        if guess == self.the_word:
            print('Well done!')
            # TODO: display needs to know if the correct word
        if guess == 'giveup':
            print(f'YOU LOSE!  The word was {self.the_word}')
            sys.exit(1)
        if guess == 'reci mi':
            print(self.the_word)
        if self.num_guesses == MAX_GUESSES:
            print('Wah wah.  So close!')
            print(f'the word was: {self.the_word}')
            sys.exit(1)
        if len(guess) > WORD_LENGTH:
            print(f'{guess} is too long, try again')
        elif len(guess) < WORD_LENGTH:
            print(f'{guess} is too short, try again')
        elif guess not in self.words:
            print(f'{guess} is not in the word list, try again')
        else:
            return True
        return False
        

def main(args):
    bordle = Bordle()
    while True:
        bordle.display_grid()
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
    sys.exit(main([]))
