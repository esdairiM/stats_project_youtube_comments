import youtube, json
import extractot
import logging.config
from datetime import datetime

# load the logging configuration
logging.config.fileConfig('logging.ini', defaults={'logfilename': 'mylog.log'})

#gettig youtube api keys
with open('youout_api_config.json','r') as config:
    configuration = json.load(config)

yout = youtube.Youtube(configuration)
videoId = '-UAvLhaF-Eg'

#res = yout.get_video_comments(videoId,maxResults=30)
comments=list()
for res in yout.get_all_comments(videoId):
    commentlist = extractot.get_comments(res)
    comments.extend(commentlist)

#to be saved in database
videoComents={
    "videoId":videoId,
    "created_at":datetime.now()
    "comments":comments
}




