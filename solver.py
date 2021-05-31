from typing import Set

from constants import DEFAULT_TRIES


class WordSet:
    def __init__(self, words: Set[str], length: int):
        if length <= 0:
            raise ValueError('Length must be positive.')

        self._wordset = set(filter(lambda x: len(x) == length, words))
        self._word_length = length
        self._pruned_letters = set()

    def incremental_wordset_prune(self, char: str, idx: int) -> None:
        if idx >= self._word_length:
            raise ValueError(f'Invalid index: {idx}. Maximum index: {self._word_length - 1}')

        if len(char) != 1:
            raise ValueError(f'Can only prune by letter.')

        if char in self._pruned_letters:
            raise ValueError(f'Letter {char} already guessed.')

        for word in self._wordset:
            if word[idx] != char:
                self._wordset.remove(word)
        return


class Solver:
    def __init__(self, length: int, tries=DEFAULT_TRIES):
        pass
