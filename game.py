import numpy as np

def str_to_np_arr(s: str):
  return np.array([ord(char) for char in s])

class Hangman():
  def __init__(
    self,
    # encode words as a numpy array, converting ascii to integers
    words: str,
  ):
    self.words = str_to_np_arr(words)
    self.filled = np.zeros(a.shape, dtype=bool)
    self.attempts = 0
    self.misses = 0
  def guess(self, char: int):
    self.attempts += 1
    idxs, = np.nonzero(self.words - char)
    if not np.any(idxs): self.misses += 1
    self.filled[idxs] = True
    return idxs
