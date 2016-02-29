from __future__ import print_function
from cpython cimport bool
from collections import defaultdict
from itertools import chain
import io


def filter_word_stream(self, sentence):
    cdef list filtered
    cdef set stop_list
    stop_list = self.config.get('stop_list', set())
    filtered = []
    for w in sentence:
        self.vocabulary[w] += 1
        if self.vocabulary[w] > self.config.get('lower_threshold', 0) and w not in stop_list:
            filtered.append(w)
    return filtered


def _read_documents(self, corpus):
    """
    If text file, treats each line as a sentence.
    If list of list, treats each list as sentence of words
    """
    if isinstance(corpus, str):
        corpus = open(corpus)

    for sentence in corpus:
        if isinstance(sentence, list):
            pass
        elif isinstance(sentence, str):
            sentence = _tokenize(sentence)
        else:
            raise TypeError("Corpus format not supported")

        yield filter_word_stream(self, sentence)

    if isinstance(corpus, io.TextIOBase):
        corpus.close()


def _tokenize(s):
    """
    Removes all URL's replacing them with 'URL'. Only keeps A-Ö 0-9.
    """
    return s.split()


cdef tuple _build_contexts(self, focus, list sentence, int i):
    cdef bool ordered, directed, is_ngrams
    cdef int left, right
    cdef tuple window_size
    cdef list context
    cdef int j
    cdef str add_word

    ordered = self.config.get('ordered', False)
    directed = self.config.get('directed', False)
    window_size = self.config['window_size']

    left = i - window_size[0] if i - window_size[0] > 0 else 0
    right = i + window_size[1] + 1 if i + window_size[1] + 1 <= len(sentence) else len(sentence)

    context = []
    for j in range(right - left):
        if left + j == i:  # skip focus word
            continue

        add_word = sentence[left+j]

        if directed:
            if left + j < i:
                add_word += '_left'
            elif left + j > i:
                add_word += '_right'

        if ordered:
            if left + j < i:
                add_word += '_' + str(j + 1)
            elif left + j > i:
                add_word += '_' + str(left + j - i)

        context.append(add_word)

    return focus, context


def _vocabularize(self, corpus):
    """
    Wraps the corpus object creating a generator that counts the vocabulary, 
    and yields the focus word along with left and right context.
    Lists as replacements of words are treated as one unit and iterated through (good for ngrams).
    """
    cdef int n, i
    cdef list sentence
    cdef str focus

    is_ngrams = self.config.get('is_ngrams', False)

    for n, sentence in enumerate(_read_documents(self, corpus)):
        if n % 1000 == 0:
            print(".", end=" ", flush=True)
        for i, focus in enumerate(sentence):
            contexts = _build_contexts(self, focus, sentence, i)
            yield contexts

def build(focus_words, context_words):
    """
    Builds a dict of dict of collocation frequencies. This is to be cythonized.
    """
    # Collect word collocation frequencies in dict of dict
    colfreqs = defaultdict(lambda: defaultdict(int))
    for focus, contexts in zip(focus_words, context_words):
        for context in contexts:
            colfreqs[focus][context] += 1

    return colfreqs
