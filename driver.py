from ntpath import join
import sys

from moviepy.video.compositing.concatenate import concatenate_videoclips
import redditors
import movie


#Connect to reddit session
reddit = redditors.get_reddit_instance()

#Get submissions
if len(sys.argv) == 2:
    sub_name = sys.argv[1]
else:
    sub_name = 'BeAmazed'

hot_submissions = redditors.get_hot_submissions(reddit, sub_name )

#filter submissions
filtered_submissions = redditors.filter_submissions(hot_submissions, min_length=5, max_length=122, total_length=600)

#download clips and gather necessary info in lists
clipNames = []
comments = []
titles = []

clipNames, comments, titles, width, height = movie.download_clips_and_get_info(reddit, filtered_submissions, directory=sub_name)
clips = movie.textify(clipNames, titles, comments,height,width, directory=sub_name)
clipsWithAudio = movie.audify(clips)
clipsWithCommentary = movie.add_commentary(clipsWithAudio)
movie.concatenate(clipsWithCommentary, sub_name)

pass