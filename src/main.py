import pprint
from src import extractot,wrapper

wrapper=wrapper.Wrapper()

yout=wrapper.get_youtube_connection()
database=wrapper.get_youtube_connection()

videoId = '-UAvLhaF-Eg'


def get_and_format_comments(videoId):
    comments = list()
    for res in yout.get_all_comments(videoId):
        commentlist = extractot.get_comments(res, videoId)
        comments.extend(commentlist)
    return comments


comments= get_and_format_comments(videoId)

pprint.pprint(comments[2:5])


