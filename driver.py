import sys

from moviepy.video.compositing.concatenate import concatenate_videoclips
import redditors
import movie



#Connect to reddit session
reddit = redditors.get_reddit_instance()

#Get submissions
if len(sys.argv) == 2:
    sub_name = sys.argv[1]
    searchType = sys.argv[2]
else:
    sub_name = "nextfuckinglevel"
    searchType = 'top'

def create_video(subName, searchType, min_ups=1000):
    submissions = redditors.get_submissions(reddit, sub_name, searchType=searchType )

    #filter submissions
    filtered_submissions = redditors.filter_submissions(submissions, min_length=5, max_length=122, total_length=600, min_ups=min_ups)

    #download clips and gather necessary info in lists
    clipNames = []
    comments = []
    titles = []

    clipNames, comments, titles, width, height = movie.download_clips_and_get_info(reddit, filtered_submissions, directory=sub_name)
    clips = movie.textify(clipNames, titles, comments,height,width, directory=sub_name)
    clipsWithAudio = movie.audify(clips)
    clipsWithCommentary = movie.add_commentary(clipsWithAudio)
    movie.concatenate(clipsWithCommentary, sub_name)

if __name__ == "__main__":
    subName = "nonononoyes"
    searchType = 'hot'
    minUps = 1000
    create_video(subName, searchType, min_ups=minUps)