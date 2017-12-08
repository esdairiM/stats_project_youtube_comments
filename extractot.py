import logging


def get_comments(json_string):
    logger = logging.getLogger(__name__)
    '''
    this methode will get you comments from a json string if there is one
    else it will do nothing
        input:
            json_string : json response from youtube data api list of comment threads    
        output:
            a list of dict 
            [
                {'auther':auther name,
                'text':the comment}
            ...]
        
    '''
    if json_string:
        comments=[]
        for item in json_string["items"]:
            comments.append(
                {
                    'auther':item["snippet"]['topLevelComment']["snippet"]["authorDisplayName"],
                    'text': item["snippet"]['topLevelComment']["snippet"]['textOriginal']
                }
            )
        logger.info('comments collected ')
        return comments;
    else:
        logger.warn('empty json string ')
        pass

