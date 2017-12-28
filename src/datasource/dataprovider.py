import logging

import googleapiclient.errors as gerrors
from googleapiclient.discovery import build


class Provider:
    def __init__(self, configuration, logger=None):
        try:
            self._logger = logger or logging.getLogger(__name__)
            self._logger.info('building the data provider')
            self._service = build(configuration["API_SERVICE_NAME"], configuration["API_VERSION"],
                                  developerKey=configuration["api_key"], cache_discovery=False)
        except gerrors.Error as e:
            self._logger.info(e._get_reason())
            raise Exception("Error initializing provider")

    def get_video_comments(self, video_id, part=['snippet'], order='relevance', maxResults=20):
        '''
        this method will attempt to fetch commentThread list from the api
        for a given videoId and return the json string, if it succeeds
        else it will pass
        input:
            :param video_id: the id of the youtube video
            :param part:(Optional) an array where you specif the response content, default is snippet, other options: replies
            :param order:(Optional) comments order, default is relevance, other option is time
            :param maxResults:(Optional) the number of the results, default is 20 max is 100
        output:part
            :return commentThread list : https://developers.google.com/youtube/v3/docs/commentThreads/list#response
        '''
        try:
            self._logger.info("fetching comments from youtube api")
            return self._service.commentThreads().list(part=','.join(part), videoId=video_id, order=order,
                                                       maxResults=maxResults).execute()
        except gerrors.Error as e:
            self._logger.info(e._get_reason())
            raise e

    def get_all_comments(self, video_id, part=['snippet'], order='relevance'):
        '''
        this method is a generator that will attempt to fetch commentThread list from the api for a given videoId
        and return the json string with a 100 elements each time if it succeeds while there is a next page token
        else it will pass.
        input:
            :param video_id: the id of the youtube video
            :param part   :(Optional)  an array where you specif the response content, default is snippet, other options: replies
            :param order  :(Optional) comments order, default is relevance, other option is time
        output:
            :return commentThread list : https://developers.google.com/youtube/v3/docs/commentThreads/list#response
        '''
        try:
            self._logger.info("fetching all comments from youtube api")
            commentThreads = self._service.commentThreads()
            request = commentThreads.list(part=','.join(part), videoId=video_id, order=order, maxResults=100)
            while request is not None:
                commentThreads_doc = request.execute()
                print("response totalResults {}".format(commentThreads_doc["pageInfo"]["totalResults"]))
                yield commentThreads_doc
                request = commentThreads.list_next(request, commentThreads_doc)
            return commentThreads_doc
        except gerrors.Error as e:
            self._logger.info(e._get_reason())
            raise e
