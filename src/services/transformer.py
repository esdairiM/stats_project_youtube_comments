import logging
from datetime import datetime
from numba import jit

from src.services.textPrecessingService import get_lang



@jit
def get_comments(json_string, video_id):
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
    logger = logging.getLogger(__name__)
    if json_string:
        comments = []
        for item in json_string["items"]:
            formated_dict = {
                'videoId': video_id,
                'created_at': datetime.now(),
                'author': item["snippet"]['topLevelComment']["snippet"]["authorDisplayName"],
                'comment': item["snippet"]['topLevelComment']["snippet"]['textOriginal'],
                'lang': get_lang(item["snippet"]['topLevelComment']["snippet"]['textOriginal']),
                'likes': item["snippet"]['topLevelComment']["snippet"]['likeCount']
            }
            comments.append(formated_dict)
        return comments
    else:
        logger.warning('empty json string ')
        pass
