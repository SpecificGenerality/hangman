import csv
import os
from typing import List

import numpy as np

from constants import MAX_DIFFICULTY, MIN_DIFFICULTY


class Generator:
  @classmethod
  def generate_word_by_frequency(cls, words: List[str], frequencies: np.array, difficulty: int) -> str:
    if difficulty < MIN_DIFFICULTY or difficulty > MAX_DIFFICULTY:
      raise ValueError(f'Difficulty must be between {MIN_DIFFICULTY} and {MAX_DIFFICULTY}, inclusive.')

    if len(words) != len(frequencies):
      raise ValueError('Mismatch in length of words and frequencies lists.')

    if len(words) < MAX_DIFFICULTY - MIN_DIFFICULTY:
      raise ValueError('Not enough words.')

    normalized_frequencies = frequencies / max(frequencies)
    sorted_idxs = np.flip(np.argsort(normalized_frequencies))
    normalized_frequencies = normalized_frequencies[sorted_idxs]
    sorted_words = np.array(words)[sorted_idxs]
    bootstrap_cdf = np.cumsum(normalized_frequencies / sum(normalized_frequencies))
    difficulty_bin_width = (max(bootstrap_cdf) - min(bootstrap_cdf)) / MAX_DIFFICULTY
    lower_bound = min(bootstrap_cdf) + (difficulty - 1) * difficulty_bin_width
    upper_bound = lower_bound + difficulty_bin_width
    lower_idx = np.where(bootstrap_cdf >= lower_bound)[0][0]
    upper_idx = np.where(bootstrap_cdf >= upper_bound)[0][0] if difficulty < MAX_DIFFICULTY else len(words)
    return np.random.choice(sorted_words[lower_idx:upper_idx])

def load_generator_csv():
  words = []
  counts = []
  with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "unigram_freq.csv")) as f:
    reader = csv.reader(f)
    _header = next(reader)
    for word,count in reader:
      words.append(word)
      counts.append(int(count))
  return words, np.array(counts)

def load_generator_txt():
  words, counts = [], []
  with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "ANC-written-count.txt")) as f:
    content = f.readlines()

  found = {}
  for line in content:
    word_info = line.split()
    word = word_info[0]
    if "'" in word or len(word) < 2 or word in found:
      continue

    found[word] = True
    words.append(word)
    counts.append(int(word_info[-1]))
  return words, np.array(counts)
