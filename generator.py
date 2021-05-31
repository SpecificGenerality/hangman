from typing import List

import numpy as np
from numpy.core.fromnumeric import sort

from constants import MAX_DIFFICULTY, MIN_DIFFICULTY


class Generator:
    @classmethod
    def generate_word_by_frequency(cls, words: List[str], frequencies: np.array, difficulty: int) -> str:
  if difficulty < MIN_DIFFICULTY or difficulty > MAX_DIFFICULTY:
    raise ValueError(f'Difficulty must be between {MIN_DIFFICULTY} and {MAX_DIFFICULTY}, inclusive.')

  if len(words) != len(frequencies):
    raise ValueError('Mismatch in length of words and frequencies lists.')

  normalized_frequencies = frequencies / max(frequencies)
  sorted_idxs = np.argsort(normalized_frequencies)
  normalized_frequencies = normalized_frequencies[sorted_idxs]
  sorted_words = np.array(words)[sorted_idxs]
  bootstrap_cdf = np.cumsum(normalized_frequencies / sum(normalized_frequencies))
  lower_bound = 0 if difficulty == 1 else (difficulty - 1) / MAX_DIFFICULTY
  upper_bound = difficulty / MAX_DIFFICULTY
  lower_idx = np.where(bootstrap_cdf >= lower_bound)[0][0]
  upper_idx = np.where(bootstrap_cdf >= upper_bound)[0][0] if difficulty < MAX_DIFFICULTY else len(words)
  return np.random.choice(sorted_words[lower_idx:upper_idx])
