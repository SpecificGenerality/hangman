import os
import random

import gensim
import gensim.downloader as api


class Hinter:
  def __init__(self, model_path: str, word: str, n_hints=100):
    if word is None:
      raise ValueError('Word cannot be None')

    self._word = word

    try:
      self._model= gensim.models.KeyedVectors.load_word2vec_format(model_path)
    except FileNotFoundError:
      model_name = os.path.split(model_path)[-1]
      self._model = api.load(model_name)

    self._hints = self._model.most_similar(self._word, topn=n_hints)

  @property
  def word(self):
    return self._word

  @word.setter
  def word(self, new_word: str):
    self._word = new_word

  def get_hint(self) -> str:
    if self._word is None:
      raise ValueError('Word not set.')

    hint = random.choice(self._hints)
    return hint
