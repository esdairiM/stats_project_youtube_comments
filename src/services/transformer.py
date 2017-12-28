import logging
from datetime import datetime
from numba import jit
from langdetect import detect,DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 0

language_dict={
    'da':'da',
    'nl':'nl',
    'en':'en',
    'di':'di',
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

def get_lang(text):
    try:
        lang=detect(text)
        if lang in language_dict.keys():
            return language_dict[lang]
        else:
            return None
    except LangDetectException as e:
        return None


@jit
def get_comments(json_string, video_id):
    logger = logging.getLogger(__name__)
    '''
        input:
            :param json_string : json response from youtube data api list of comment threads  
            :param video_id :
        output:
            :return list of dict :
            [
                {
                'videoId':video_id,
                'created_at': datetime.now(),
                'auther':auther name,
                'text':the comment,
                'likes':comment like count
                }
            ...]
        
    '''
    if json_string:
        comments = []
        for item in json_string["items"]:
            comments.append(
                {
                    'videoId': video_id,
                    'created_at': datetime.now(),
                    'author': item["snippet"]['topLevelComment']["snippet"]["authorDisplayName"],
                    'lang':get_lang(item["snippet"]['topLevelComment']["snippet"]['textOriginal']),
                    'comment': item["snippet"]['topLevelComment']["snippet"]['textOriginal'],
                    'likes':item["snippet"]['topLevelComment']["snippet"]['likeCount']
                }
            )
        return comments
    else:
        logger.warn('empty json string ')
        pass
