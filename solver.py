from typing import Set

from constants import DEFAULT_MAX_MISSES


class WordSet:
    def __init__(self, words: Set[str], length: int):
        if length <= 0:
            raise ValueError('Length must be positive.')

        self._wordset = set(filter(lambda x: len(x) == length, words))
        self._word_length = length
        self._pruned_letters = set()

    def incremental_prune(self, letter: str) -> None:
        if len(letter) != 1:
            raise ValueError(f'Can only prune by letter.')

        if letter in self._pruned_letters:
            raise ValueError(f'Letter {letter} already guessed.')

        removed = set()
        for word in self._wordset:
            if letter in word:
                removed.add(word)

        self._wordset = self._wordset.difference(removed)
        self._pruned_letters.add(letter)
        return


class Solver:
    def __init__(self, length: int, tries=DEFAULT_MAX_MISSES):
        pass
