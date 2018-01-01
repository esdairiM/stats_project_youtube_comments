from collections import Counter
from logging import getLogger as _getLogger

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


def popular_words(comments, number):
    _logger = _getLogger(__name__)
    _logger.info("initializing LanguageProcessing service")
    counter = counte_words(comments)
    return counter.most_common(number)


def counte_words(comments)->Counter:
    comments_text = list(map(lambda cmnt: cmnt["comment"], comments))
    counter = Counter(" ".join(comments_text).split(" "))
    return counter


def prepare_text(comment: str, lang=None)->list:
    # comment["lang"] is none if it's not supported by mongodb
    # we have to detect language to remove stope words and stemme
    try:
        lang = lang if lang != "none" and lang!= None else detect(comment)
    except  LangDetectException as e:
        _getLogger(__name__).warning(str(e))
        pass
    # tokenize comment text
    words = tokenize(comment)
    # remove numbers and punctuation
    filtred_words = remove_punctuation(words)
    # remove stop words
    filtred_words = remove_stop_words(filtred_words, lang)
    # stemme words
    filtred_words = stemme_words(filtred_words, lang)
    return filtred_words


def prepare_text_list(comments: list)->dict:
    authors=list(map(lambda cmnt:cmnt["author"],comments))
    comment_text=list(map(lambda cmnt:cmnt["comment"],comments))
    return {"author": authors, "comments": comment_text}


def stemme_words(words: list, lang) -> list:
    if lang is not None and lang in _lang_names.keys():
        stemmer = _SnowballStemmer(_lang_names[lang])
        words = list(map(lambda word:stemmer.stem(word),words))
    return words


def stemme_text(text: str, returnList=True, lang=None):
    try:
        lang = lang if lang != "none" else detect(comment)
    except  LangDetectException as e:
        _getLogger(__name__).warning(str(e))
        pass
    words = tokenize(text)
    words=stemme_words(words,lang)
    if returnList:
        return words
    else:
        return " ".join(words)


def remove_stop_words(words: list, lang) -> list:
    if lang is not None and lang in sw_languages_mapping:
        words=list(filter(lambda word: word not in _get_stop_words(lang),words))
        #words = [word for word in words if word not in _get_stop_words(lang)]
    return words


# def remove_text_stop_words(text: str, lang="", returnList=True):
#     words = tokenize(text)
#     lang = lang if lang != "" else get_lang(text)
#     if noStopWords and lang is not None and lang in sw_languages_mapping:
#         words = [word for word in words if word not in _get_stop_words(lang)]
#     if returnList:
#         return words
#     else:
#         return " ".join(words)


def remove_punctuation(words)->list:
    if remove_numeric:
        filtred_words=list(filter(lambda word:word.isalpha,words))
        #filtred_words = [word for word in words if word.isalpha()]
    else:
        filtred_words = list(filter(lambda word: word.isalnum(), words))
    return filtred_words


def tokenize(text) -> list:
    words = _word_tokenize(text.lower())
    return words


def get_lang(text, main_language="en")->str:
    try:
        lang = detect(text)
        if lang not in _mongo_langs:
            lang = main_language
        return lang
    except LangDetectException as e:
        _getLogger(__name__).warning(str(e))
        return main_language
