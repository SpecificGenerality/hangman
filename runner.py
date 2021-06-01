import argparse

from constants import DEFAULT_MAX_MISSES
from game import Hangman, it_to_str
from generator import Generator, load_generator_csv
from solver import Solver, WordSet


def get_letter(prompt: str) -> int:
  while True:
    try:
      letter = str(input(prompt))
      if len(letter) != 1:
        continue
      letter = letter.lower()
      if ord(letter) < ord('a') or ord(letter) > ord('z'):
        continue
      break
    except ValueError:
      print('Letters only please.')

  return ord(letter)

def run(difficulty: int, max_misses: int, word: str = None):
  words, counts = load_generator_csv()
  if word is None:
    word = Generator.generate_word_by_frequency(words, counts, difficulty)

  G = Hangman(word, max_misses)
  while not G.gameover:
    print(G)
    letter = get_letter('Enter your guess: ')
    G.guess(letter)

  if G.is_win:
    print('You won!')
  else:
    print(f'{G.misses} of {max_misses} used.\nYou lost :(')

  print(f'The word: {it_to_str(G.words)}')

def solve(difficulty: int, max_misses: int, word: str = None):
  words, counts = load_generator_csv()
  if word is None:
    word = Generator.generate_word_by_frequency(words, counts, difficulty)

  G = Hangman(word, max_misses)
  WS = WordSet(words, len(word))
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
