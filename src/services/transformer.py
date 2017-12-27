import logging
from datetime import datetime
from numba import jit
'''this method will attempt to get you comments from a json string
if fail it will pass'''

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
                    'auther': item["snippet"]['topLevelComment']["snippet"]["authorDisplayName"],
                    'comment': item["snippet"]['topLevelComment']["snippet"]['textOriginal'],
                    'likes':item["snippet"]['topLevelComment']["snippet"]['likeCount']
                }
            )
        return comments
    else:
        logger.warn('empty json string ')
        pass
