

# key:lang_detect module return,
# value:mongodb supported abbreviation
language_abreviation={
    'da':'da',
    'nl':'nl',
    'en':'en',
    'fi':'fi',
    'fr':'fr',
    'de':'de',
    'hu':'hu',
    'it':'it',
    'nb':'nb',
    'pt':'pt',
    'ro':'ro',
    'ru':'ru',
    'es':'es',
    'sv':'sv',
    'tr':'tr',
    'ar':'ara',
    'fa':'pes',
    'ur':'urd'
}
# key:mongodb language abbreviation
# value:nltk SnowballStemmer language equivalent
language_long_name={
    'da':'danish',
    'nl':'dutch',
    'en':'english',
    'fi':'finnish',
    'fr':'french',
    'de':'german',
    'hu':'hungarian',
    'it':'italian',
    'nb':'norwegian',
    'pt':'portuguese',
    'ro':'romanian',
    'ru':'russian',
    'es':'spanish',
    'sv':'swedish',
    'ar':'arabic'
}

def inverse_dictionary(lang_dict):
    inv_dict=dict()
    for key, val in lang_dict.items():
        inv_dict.update({val:key})
    return inv_dict;