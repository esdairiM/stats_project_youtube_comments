from googleapiclient.discovery import build
import googleapiclient.errors as gerrors
import logging


class Youtube:
    def __init__(self,configuration,logger=None):
        self._logger_ = logger or logging.getLogger(__name__)
        self._logger.info('building the data provider')
        self._service_ = build(configuration["API_SERVICE_NAME"],configuration["API_VERSION"], configuration["developerKey"], cache_discovery=False)

    def get_video_comments(self,videoId, part=['snippet'], order='relevance', maxResults=20):
        '''
        this methode will attempte to fetch commentThread list from the api for a given videoId
        and return the json string if it succeds
        else it will pass

        input:
            part   : the response array of content, defualt snippint option replies
            videoId: the id of the youtube video
            order  : comments order, default is relevance, other option is time
            maxResults: the number of the results, default is 20 max is 100
        output:
            commentThread list : https://developers.google.com/youtube/v3/docs/commentThreads/list#response
        '''
        try:
            self._logger.info("fetching comments from youtube api")
            return self._service_.commentThreads().list(part=','.join(part), videoId=videoId, order=order, maxResults=maxResults).execute()
        except gerrors.Error as e:
            self._logger.info(e._get_reason())
            pass

    def get_all_comments(self, videoId, part=['snippet'], order='relevance'):
        '''
        this methode is a generator that will attempte to fetch commentThread list from the api for a given videoId
        and return the json string with a 100 elements each time if it succeds while there is a next page token
        else it will pass

        input:
            part   : the response array of content, defualt snippint option replies
            videoId: the id of the youtube video
            order  : comments order, default is relevance, other option is time
        output:
            commentThread list : https://developers.google.com/youtube/v3/docs/commentThreads/list#response
        '''
        try:
            self._logger.info("fetching all comments from youtube api")
            commentThreads= self._service_.commentThreads()
            request = commentThreads.list(part=','.join(part), videoId=videoId, order=order, maxResults=100)
            while request is not None:
                commentThreads_doc = request.execute()
                yield commentThreads_doc
                request =commentThreads.list_next(request,commentThreads_doc)
            return commentThreads_doc
        except gerrors.Error as e:
            self._logger.info(e._get_reason())
            pass
        
    

