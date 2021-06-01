from typing import Iterable

import numpy as np

from constants import DEFAULT_MAX_MISSES


def str_to_np_arr(s: str) -> np.array:
  return np.array([ord(char) for char in s])

def it_to_str(arr: Iterable, delim: str='') -> str:
  return delim.join(chr(ord_char) for ord_char in arr)

class Hangman():
  def __init__(
    self,
    # encode words as a numpy array, converting ascii to integers
    words: str,
    max_misses: int = DEFAULT_MAX_MISSES
  ):
    self.words = str_to_np_arr(words)
    self.filled = np.zeros(self.words.shape, dtype=bool)
    self.attempts = 0
    self.misses = 0
    self.max_misses = max_misses
    self.guesses = []

  @property
  def gameover(self):
    return self.misses >= self.max_misses or np.all(self.filled)

  @property
  def is_win(self):
    return np.all(self.filled) and self.misses < self.max_misses

  def guess(self, char: int) -> np.array:
    if self.gameover:
      raise ValueError('No more guesses remaining.')

    if char in self.guesses: return []

    self.attempts += 1
    idxs = np.where((self.words - char) == 0)[0]
    if len(idxs) == 0: self.misses += 1
    self.filled[idxs] = True
    self.guesses.append(char)
    return idxs

  def __len__(self): return len(self.words)

  def __str__(self):
    partial_word = np.array([ord('_') for _ in range(len(self.words))])
    if np.any(self.filled):
      filled_idxs = np.where(self.filled)[0]
      partial_word[filled_idxs] = self.words[filled_idxs]
    partial_word = it_to_str(partial_word, ' ')

    prev_guesses = it_to_str(self.guesses)
    miss_msg = f'{self.misses} of {self.max_misses} used.'
    return '\n'.join((partial_word, prev_guesses, miss_msg))
