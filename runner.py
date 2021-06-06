import argparse

from constants import DEFAULT_MAX_MISSES
from game import Hangman, it_to_str
from generator import (Generator, load_generator_csv, load_generator_txt,
                       preprocess)
from hints import Hinter
from solver import FreqWordSet, Solver, WordSet


def get_letter(prompt: str) -> int:
  while True:
    try:
      letter = str(input(prompt))
      if len(letter) != 1:
        continue
      letter = letter.lower()
      # Bypass for hints
      if ord(letter) == ord('?'):
        break
      if ord(letter) < ord('a') or ord(letter) > ord('z'):
        continue
      break
    except ValueError:
      print('Letters only please.')

  return ord(letter)

def get_bool(prompt: str) -> bool:
  while True:
    try:
      res = str(input(prompt))
      res = res.lower()
      if res in ['y','yes', 'true', 't']:
        return True
      elif res in ['n', 'no', 'false', 'f']:
        return False
      else: continue
    except ValueError:
      print('Strings only please')

def run(difficulty: int, max_misses: int, word: str = None):
  words, counts = load_generator_txt()
  words, counts = preprocess(words, counts)

  if word is None:
    word = Generator.generate_word_by_frequency(words, counts, difficulty)

  hinter = Hinter('glove-wiki-gigaword-300', word)
  playing = True
  while playing:
    G = Hangman(word, max_misses)
    hinter.word = word
    while not G.gameover:
      print(G)
      letter = get_letter('Enter your guess ("?" for hint): ')
      if letter == ord('?'):
        hint_word = hinter.get_hint()
        print(f'The word is similar in meaning to: {hint_word}')
        continue
      G.guess(letter)

    if G.is_win:
      print('You won!')
    else:
      print(f'{G.misses} of {max_misses} used.\nYou lost :(')

    playing = get_bool('Play again? [Y/N]')
    word = Generator.generate_word_by_frequency(words, counts, difficulty)


    print(f'The word: {it_to_str(G.words)}')

def solve(difficulty: int, max_misses: int, word: str = None):
  words, counts = load_generator_txt()
  words, counts = preprocess(words, counts)
  if word is None:
    word = Generator.generate_word_by_frequency(words, counts, difficulty)

  G = Hangman(word, max_misses)
  WS = FreqWordSet(words, counts, len(word))
  S = Solver(G, WS)
  print("Word is", word)
  while not G.gameover:
    guess = S.step()
    print(f"Guessing: {guess}")
  if G.is_win: print("Found!")
  else: print("Lost!")

  return

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
    '-d', '--difficulty', type=int, choices=[i for i in range(1, 11)], help='Difficulty',
    default=1,
  )
  parser.add_argument('--max-misses', type=int, default=DEFAULT_MAX_MISSES)
  parser.add_argument('--solve', action='store_true')
  parser.add_argument('--word', type=str, default=None)

  args = parser.parse_args()

  if args.solve: solve(args.difficulty, args.max_misses, args.word)
  else: run(args.difficulty, args.max_misses, args.word)
