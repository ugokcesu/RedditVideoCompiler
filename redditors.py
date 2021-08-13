import requests
import praw
import json
from praw.reddit import Reddit
import youtube_dl
from datetime import datetime



def get_reddit_instance():
    credentials = json.load(open("credentials.json"))
    return praw.Reddit(client_id=credentials['client_id'], client_secret=credentials['client_secret'], user_agent=credentials['user_agent'])

def get_submissions(redditInstance, subredditName='NextFuckingLevel', searchType='hot', limit=2000):
    if searchType == 'hot':
        return redditInstance.subreddit(subredditName).hot(limit=limit)
    if searchType == 'top':
        return redditInstance.subreddit(subredditName).top('week', limit=limit)

def filter_submissions(submissions, min_length=10, max_length=180, total_length=120, min_upratio=0.95, min_ups=1000):
    MAX_AUDIO_LENGTH = 30
    runningTotalTime = 0
    subsList = []
    for s in submissions:
        if runningTotalTime > total_length:
            break
        #filter out stickied, nsfw, and non-video posts
        if s.stickied or not s.is_video or s.over_18:
            continue
        #Now apply upvote filters
        if s.ups < min_ups or s.upvote_ratio < min_upratio:
            continue  
        duration = s.media['reddit_video']['duration']
        if duration > max_length or duration < min_length:
            continue
        has_audio = "_AUDIO" in requests.get(s.media['reddit_video']['hls_url']).text
        if has_audio and duration > MAX_AUDIO_LENGTH:
            continue
        
        subsList.append(s)
        runningTotalTime += duration
    print(len(subsList))
    return subsList

def comment_extractor(redditInstance, id, ratio=0.004, max_length=300):
    commentList = []
    submission = redditInstance.submission(id)
    min_ups = submission.ups * ratio
    submission.comment_sort='top'
    for comment in submission.comments:
        if isinstance(comment, praw.models.MoreComments):
            break
        if comment.ups > min_ups and len(comment.body) < max_length:
            commentList.append(comment.body)
            for reply in comment.replies:
                if isinstance(reply, praw.models.MoreComments):
                    break
                if reply.ups>min_ups/2 and len(reply.body) < max_length:
                    commentList.append(">>" + reply.body)
    return commentList

def download_clip(redditInstance, id, fileName):
    submission = redditInstance.submission(id)
    url = submission.url
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': fileName+'.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])




options = {
'min_length': 3,
'max_length': 30,
'total_length': 60,
'min_upratio': 0.95,
'min_ups': 1000
}

 