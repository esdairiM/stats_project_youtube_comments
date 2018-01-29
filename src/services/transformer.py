import logging
from datetime import datetime

from numba import jit

from src.services.textPrecessingService import get_lang, prepare_text


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
    if json_string:
        print('transformer called')
        comments = []
        for item in json_string["items"]:
            lang = get_lang(item["snippet"]['topLevelComment']["snippet"]['textOriginal'])
            original_comment = item["snippet"]['topLevelComment']["snippet"]['textOriginal']
            comment = prepare_text(original_comment)
            formated_dict = {
                'videoId': video_id,
                'created_at': datetime.now(),
                'author': item["snippet"]['topLevelComment']["snippet"]["authorDisplayName"],
                'comment': " ".join(comment),
                'original_comment': original_comment,
                'lang': lang,
                'authorChannelId': item["snippet"]['topLevelComment']["snippet"]["authorChannelId"]["value"],
                'likes': item["snippet"]['topLevelComment']["snippet"]['likeCount']
            }
            comments.append(formated_dict)
        return comments
    else:
        logging.getLogger(__name__).warning('empty json string ')
        pass


def tansform_video_data(jsondata, video_id):
    logger = logging.getLogger(__name__)
    if jsondata:
        item=jsondata['items'][0]
        formated_dict = {
            'videoId': video_id,
            'publishedAt': item["snippet"]["publishedAt"],
            'title': item["snippet"]['title'],
            'description': item["snippet"]["description"],
            'videoUrl':'https://www.youtube.com/watch?v='+video_id,
            'channelUrl': 'https://www.youtube.com/channel/'+item["snippet"]["channelId"],
            'viewCount': item["statistics"]["viewCount"],
            'likeCount': item["statistics"]["likeCount"],
            'dislikeCount': item["statistics"]["dislikeCount"],
            'commentCount': item["statistics"]["commentCount"]
        }
        return formated_dict
    else:
        logger.warning('empty json string ')
        pass
