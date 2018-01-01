from collections import Counter
from logging import getLogger as _getLogger
from multiprocessing import Pool
from os import cpu_count as _cpu_count

from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from nltk.stem import SnowballStemmer as _SnowballStemmer
from nltk.tokenize import word_tokenize as _word_tokenize
from stop_words import LANGUAGE_MAPPING as sw_languages_mapping
from stop_words import get_stop_words as _get_stop_words

from src.datastore.languagesAbreviationMapping import language_long_name as _lang_names
from src.datastore.languagesAbreviationMapping import mongodb_supported_languages as _mongo_langs

'''
this module provides text processing functions:
    tokenizing,
    removing punctuation and numeric unless remove_numeric is set to False
    remove stop words unless noStopWords is set to False
    stemme words unless stemme is set to False
this module support removing stop words and stemming for 15 languages:
'arabic','danish','dutch', 'english','finnish','french','german','hungarian','italian',
 'norwegian','porter','portuguese','romanian','russian','spanish','swedish'
'''

# force lang_detect to choose one language, throws exception is it can't
DetectorFactory.seed = 0

remove_numeric: bool = True
noStopWords: bool = True
stemme: bool = True


def popular_words(comments, number, rm_numeric=True, rm_StopWords=True, stemme_text=True):
    _logger = _getLogger(__name__)
    _logger.info("initializing LanguageProcessing service")
    global remove_numeric, noStopWords, stemme
    remove_numeric = rm_numeric
    noStopWords = rm_StopWords
    stemme = stemme_text
    counter = parallel_counter(comments)
    return counter.most_common(number)


def parallel_counter(comments):
    pools = Pool(_cpu_count())
    counts = pools.imap_unordered(_count, comments)
    counter = _summe(counts)
    return counter


def _count(comment):
    filtred_words = prepare_words(comment)
    counter = Counter(filtred_words)
    return counter


def _summe(result):
    count = Counter()
    for re in result:
        count += re
    return count


def prepare_words(comment, lang=None):
    # comment["lang"] is none if it's not supported by mongodb
    # we have to detect language to remove stope words and stemme
    try:
        lang = comment["lang"] if comment["lang"] != "none" else detect(comment)
    except  LangDetectException as e:
        _getLogger(__name__).warning(str(e))
        pass
    # tokenize comment text
    words = tokenize(comment["comment"])
    # remove numbers and punctuation
    filtred_words = remove_punctuation(words)
    # remove stop words
    filtred_words = remove_stop_words(filtred_words, lang)
    # stemme words
    filtred_words = stemme_words(filtred_words, lang)
    return filtred_words


def prepare_texts(comments):
    filtred_comments=[]
    authors=[]
    for comment in comments:
        authors.append(comment["author"])
        filtred_comments.append(" ".join(prepare_words(comment)))
    return {"author":authors,"comments":filtred_comments}


def stemme_words(words: list, lang) -> list:
    if stemme and lang is not None and lang in _lang_names.keys():
        stemmer = _SnowballStemmer(_lang_names[lang])
        words = [stemmer.stem(word) for word in words]
    return words


def stemme_text(text: str, returnList=True, lang=""):
    words = tokenize(text)
    lang = lang if lang != "" else get_lang(text)
    if stemme and lang is not None and lang in _lang_names.keys():
        stemmer = _SnowballStemmer(_lang_names[lang])
        words = [stemmer.stem(word) for word in words]
    if returnList:
        return words
    else:
        return " ".join(words)


def remove_stop_words(words: list, lang) -> list:
    if noStopWords and lang is not None and lang in sw_languages_mapping:
        words = [word for word in words if word not in _get_stop_words(lang)]
    return words


def remove_text_stop_words(text: str, lang="", returnList=True):
    words = tokenize(text)
    lang = lang if lang != "" else get_lang(text)
    if noStopWords and lang is not None and lang in sw_languages_mapping:
        words = [word for word in words if word not in _get_stop_words(lang)]
    if returnList:
        return words
    else:
        return " ".join(words)


def remove_punctuation(words):
    if remove_numeric:
        filtred_words = [word for word in words if word.isalpha()]
    else:
        filtred_words = [word for word in words if word.isalnum()]
    return filtred_words


def tokenize(text) -> list:
    words = _word_tokenize(text.lower())
    return words


def get_lang(text, main_language="en"):
    try:
        lang = detect(text)
        if lang not in _mongo_langs:
            lang = main_language
        return lang
    except LangDetectException as e:
        _getLogger(__name__).warning(str(e))
        return main_language