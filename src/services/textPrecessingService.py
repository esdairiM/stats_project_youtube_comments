from collections import Counter
from logging import getLogger as _getLogger
from multiprocessing import Pool
from os import cpu_count as _cpu_count
from nltk.tokenize import word_tokenize as _word_tokenize
from nltk.stem import SnowballStemmer as _SnowballStemmer
from stop_words import get_stop_words as _get_stop_words

from src.datastore.languagesAbreviationMapping import language_long_name as _lang_names
from src.datastore.languagesAbreviationMapping import language_abreviation as _lang_abrev
from src.datastore.languagesAbreviationMapping import inverse_dictionary as _inverse_dictionary


_remove_numeric: bool
_noStopWords: bool
_stemme: bool


def get_common_words(comments, number, remove_numeric=True,noStopWords=True,stemme=True):
    _logger = _getLogger(__name__)
    _logger.info("initializing LanguageProcessing service")
    global _remove_numeric,_noStopWords,_stemme
    _remove_numeric = remove_numeric
    _noStopWords=noStopWords
    _stemme=stemme
    pools = Pool(_cpu_count())
    counts = pools.imap_unordered(_count_words, comments)
    counter = _summe(counts)
    return counter.most_common(number)


def _count_words(comment):
    # tokenize comment text
    words = _tokenize(comment["comment"])
    filtred_words = _prepare_words(words,comment["lang"])
    counter = Counter(filtred_words)
    return counter


def _summe(result):
    count = Counter()
    for re in result:
        count += re
    return count


def _prepare_words(words,lang):
    # remove numbers and punctuation
    filtred_words = _remove_punctuation(words)
    # remove stop words
    filtred_words = _remove_stop_words(filtred_words, lang)
    #stemme words
    filtred_words = _stemme_words(filtred_words, lang)
    return filtred_words


def _stemme_words(filtred_words, lang):
    if _stemme and lang is not None and lang in _lang_names.keys():
        stemmer = _SnowballStemmer(_lang_names[lang])
        filtred_words = [stemmer.stem(word) for word in filtred_words]
    return filtred_words


def _remove_stop_words(filtred_words, lang):
    if _noStopWords and lang is not None:
        inversed_lang_abrev=_inverse_dictionary(_lang_abrev)
        filtred_words = [word for word in filtred_words if word not in _get_stop_words(inversed_lang_abrev[lang])]
    return filtred_words


def _remove_punctuation(words):
    if _remove_numeric:
        filtred_words = [word for word in words if word.isalpha()]
    else:
        filtred_words = [word for word in words if word.isalnum()]
    return filtred_words


def _tokenize(text):
    words = _word_tokenize(text.lower())
    return words
