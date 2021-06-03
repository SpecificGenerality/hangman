import random
from typing import List, Set

import numpy as np
import pandas as pd

from constants import ALL_CHARS
from game import Hangman


class WordSet:
  def __init__(self, words: Set[str], length: int):
    if length <= 0:
      raise ValueError('Length must be positive.')

    self._wordset = set(filter(lambda x: len(x) == length, words))
    self._word_length = length
    self._pruned_letters = set()

  def prune(self, letter: str, idxs: np.array) -> None:
    if len(letter) != 1: raise ValueError(f'Can only prune by letter.')

    if letter in self._pruned_letters: raise ValueError(f'Letter {letter} already guessed.')

    removed = set()
    for word in self._wordset:
      should_rm = any(char == letter for i, char in enumerate(word) if i not in idxs)
      if should_rm: removed.add(word)

    self._wordset = self._wordset.difference(removed)
    self._pruned_letters.add(letter)
    return

  def best_curr(self) -> str:
    counts = {}
    for word in self._wordset:
      for char in word:
        counts[char] = counts.get(char, 0) + 1

    for letter in self._pruned_letters: counts.pop(letter, None)
    if len(counts) == 0:
      return chr(random.choice([c for c in ALL_CHARS if chr(c) not in self._pruned_letters]))
    return max(counts.keys(), key=lambda k: counts[k])

  def __len__(self): return self._word_length


class FreqWordSet(WordSet):
  def __init__(self, words: List[str], freq: np.array, length: int):
    super().__init__(set(words), length)

    self._freq_table = pd.DataFrame({'words': words, 'counts': freq}).set_index('words')
    self._freq_table = self._freq_table[self._freq_table.index.str.len() == length]

  def prune(self, letter: str, idxs: np.array) -> None:
    super().prune(letter, idxs)
    self._freq_table = self._freq_table[self._freq_table.index.isin(self._wordset)]
    return

  def best_curr(self) -> str:
    if self._freq_table.empty:
      return super().best_curr()

    total_count: int = self._freq_table['counts'].sum()
    counts = {}
    for word in self._wordset:
      for char in word:
        counts[char] = counts.get(char, 0) + self._freq_table.loc[word]['counts'] / total_count

    for letter in self._pruned_letters: counts.pop(letter, None)
    if len(counts) == 0:
      return chr(random.choice([c for c in ALL_CHARS if chr(c) not in self._pruned_letters]))

    normalization_constant = sum(counts.values())
    pmf = np.array([_ for _ in counts.values()]) / normalization_constant
    return np.random.choice([_ for _ in counts.keys()], p=pmf)


class Solver:
  def __init__(
    self,
    game: Hangman,
    word_set: WordSet,
  ):
    assert(len(game) == len(word_set))
    self.game = game
    self.word_set = word_set

  def step(self):
    next_char = self.word_set.best_curr()
    idxs = self.game.guess(ord(next_char))
    self.word_set.prune(next_char, idxs)

    return next_char
