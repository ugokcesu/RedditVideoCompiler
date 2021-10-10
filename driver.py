import sys

from moviepy.video.compositing.concatenate import concatenate_videoclips
import redditors
import movie
import praw


def create_video(reddit, sub_name, searchType, min_ups=1000):
    submissions = redditors.get_submissions(reddit, sub_name, searchType=searchType )

    #3 FILTER SUBMISSIONS
    filtered_submissions = redditors.filter_submissions(submissions, min_length=5, max_length=122, total_length=600, min_ups=min_ups)

    #download clips and gather necessary info in lists
    clipNames = []
    comments = []
    titles = []

    #4 DOWNLOAD CLIPS AND GET INFO
    clipNames, comments, titles, width, height = movie.download_clips_and_get_info(reddit, filtered_submissions, directory=sub_name)
    
    #5 TEXTIFY (ADD TITLE & COMMENTS)
    clips = movie.textify(clipNames, titles, comments,height,width, directory=sub_name)
    #6 AUDIFY (ADD FREE MUSIC)
    clipsWithAudio = movie.audify(clips)
    #7 ADD COMMENTARY (GREETING RECORDING)
    clipsWithCommentary = movie.add_commentary(clipsWithAudio)
    #8 CONCATENATE
    movie.concatenate(clipsWithCommentary, sub_name)

if __name__ == "__main__":
#    if len(sys.argv) == 2:
#        sub_name = sys.argv[1]
#        searchType = sys.argv[2]
#    else:
#        sub_name = "all"
#        searchType = 'top'


    #1 GET REDDIT INSTANCE
    reddit = redditors.get_reddit_instance()
    for subName in [ 'all', 'unexpected', 'nextfuckinglevel', 'beamazed']:#'nonononoyes', 'natureisfuckinglit', 'damnthatsinteresting',
        searchType = 'hot'
        minUps = 1000
        #2 CREATE VIDEO
        create_video(reddit, subName, searchType, min_ups=minUps)

   