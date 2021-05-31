import argparse

from constants import DEFAULT_MAX_MISSES
from game import Hangman, it_to_str
from generator import Generator, load_generator_csv


def get_letter(prompt: str) -> int:
  while True:
    try:
      letter = str(input(prompt))
      if len(letter) != 1:
        continue
      letter = letter.lower()
      if ord(letter) - ord('a') < 0 or ord(letter) - ord('a') >= 26:
        continue
      break
    except ValueError:
      print('Letters only please.')

  return ord(letter)

def run(difficulty: int, max_misses: int):
  words, counts = load_generator_csv()
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

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', type=int, choices=[i for i in range(1, 11)], help='Difficulty')
  parser.add_argument('--max_misses', type=int, default=DEFAULT_MAX_MISSES)

  args = parser.parse_args()

  run(args.d, args.max_misses)
