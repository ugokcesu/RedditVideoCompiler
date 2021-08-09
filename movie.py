import random
import re
from pathlib import Path
from  os import getcwd, path, listdir


import youtube_dl
import moviepy


from moviepy.editor import *

import redditors

MARGIN_SIZE = 70
FONT_SIZE = 40
COLORS = [ '#F80000', '#39FF13' , '#FED985', '#61B5CB', '#D5A0C4', '#73A5D6']
FONTS = [ 'Comic-Sans-MS', 'Calibri-Bold', 'Elephant', 'Cooper-Black']

def trim_comments(comments, maxChars):
    commentsTrimmed = []
    for comment in comments:
        if comment[0:2] != ">>":
            comment = '-' + comment
        end = len(comment)
        start = 0
        while end-start > maxChars:
            index = comment[start:start+maxChars].rfind(' ')
            if index == -1 or index == 0:
                index = maxChars
            commentsTrimmed.append(comment[start:start+index])
            start += index
        commentsTrimmed.append(comment[start:])
    return commentsTrimmed

def censor_comments(comments):
    censoredComments = []
    badWords = [('fuck', 'f*ck'), ('shit', 'sh*t'), ('ass', 'a**'), ('bitch', 'b*tch'), ('pussy', 'p*ssy'), ('dick', 'd*ck'), ('nigger', 'n*gga'), ('cunt', 'c*nt')]
    for comment in comments:
        for word, replacement in badWords:
            comment = re.sub(word, replacement,comment, flags=re.IGNORECASE)
        censoredComments.append(comment)
    return censoredComments



def add_subtitles(videoFile, title, comments, maxHeight, maxWidth):
    vid = VideoFileClip(videoFile)
    #vid = vid.fx(vfx.mirror_x)
    #add side margins
    width = vid.size[0]
    if width > maxWidth:
        maxWidth = width
    padding = (maxWidth - width) // 2

    vid = vid.margin(left=padding, right=maxWidth - width - padding, bottom=MARGIN_SIZE, top=MARGIN_SIZE)

    duration = vid.duration
    width = vid.size[0]
    maxChars = int(width / FONT_SIZE * 2 * 1.0)
    fontSize = int(width*2*2.0/len(title))
    fontSize = FONT_SIZE if fontSize > FONT_SIZE else fontSize
    fontSize = 20 if fontSize < 20 else fontSize
    if len(title) > maxChars:
        index = title[:maxChars].rfind(' ')
        title= title[:index] + "\n" + title[index+1:]

    titleText = TextClip(title, fontsize=fontSize, color='white', font='Amatic-Bold') \
        .set_start(0).set_end(duration).set_position('top')

    commentsCensored = censor_comments(comments)
    commentsTrimmed = trim_comments(commentsCensored, maxChars)
    
    

    time_pointer = 0
    textClip = []
    almost_done = False
    for comment in commentsTrimmed:
        if comment[0] == '-' or comment[0]=='>':
            font = random.choice(FONTS)
            color = random.choice(COLORS)
        required_time = len(comment.split())/3 + 1
        if required_time > duration - time_pointer:
            required_time = duration - time_pointer
            almost_done = True

        if duration - time_pointer >= required_time:
            textClip.append(TextClip(comment, fontsize=FONT_SIZE, font=font, color=color)
            .set_start(time_pointer)
            .set_end(time_pointer + required_time)
            .set_position('bottom'))
            time_pointer += required_time
        if almost_done:
            break
    video = CompositeVideoClip([vid, titleText, *textClip])
    return video
    #video.write_videofile(videoFile.split(".")[0] + "_withtext.mp4")

def download_clips_and_get_info(redditInstance, filtered_submissions, directory=""):
    clipNames = []
    comments = []
    titles = []
    heights = []
    widths = []

    if directory != "":
        Path(path.join(getcwd(), directory)).mkdir(parents=True, exist_ok=True)

    for counter,submission in enumerate(filtered_submissions):
        clipNames.append(path.join(directory,str(counter)+".mp4"))
        comments.append(redditors.comment_extractor(redditInstance, submission.id))
        titles.append(submission.title)
        heights.append(submission.media['reddit_video']['height'])
        widths.append(submission.media['reddit_video']['width'])
        redditors.download_clip(redditInstance, submission.id,  path.join(directory, str(counter)))
        
    return clipNames, comments, titles, max(widths), max(heights)

def textify(clipNames, titles, comments,height,width, directory):
    clips = []
    for counter in range(len(clipNames)):
        clips.append(add_subtitles(clipNames[counter], titles[counter], comments[counter],height, width))
    return clips
    #final = concatenate_videoclips(clips, method='compose')
    #final.write_videofile(path.join(directory,"final.mp4"))

def audify(clips, overwriteAll=True):
    clipsWithAudio = []
    for clip in clips:
        if clip.audio is None or overwriteAll:
            audioClip = get_audio_clip(clip.duration)
            audioClip = audioClip.volumex(0.7) 
            clipsWithAudio.append(clip.set_audio(audioClip))
        else:
            clipsWithAudio.append(clip)
    return clipsWithAudio

def add_commentary(clips):
    commentarizedClips = []
    first = True
    for clip in clips:
        if first:
            commentary = AudioFileClip(hello_picker())
            first = False
        else:
            commentary = AudioFileClip(comment_picker())
            commentary = commentary.volumex(2) 
        conc = concatenate_audioclips([commentary, clip.audio.subclip(commentary.duration,clip.duration)])
        commentarizedClips.append(clip.set_audio(conc))
    return commentarizedClips

def concatenate(clips, directory):
    final = concatenate_videoclips(clips, method='compose')
    final.write_videofile(path.join(directory,"final.mp4"))


def mp3_picker():
    return path.join("audio/",random.choice(listdir("audio/"))) #change dir name to whatever

def hello_picker():
    return path.join("Hello/", random.choice(listdir("Hello/")))

def comment_picker():
    return path.join("recordings/",random.choice(listdir("recordings/")))

def get_audio_clip(desiredDuration):
    counter = 0
    while counter < 10:
        counter +=1
        file = mp3_picker()
        aud = AudioFileClip(file)
        if aud.duration > desiredDuration:
            return aud.set_duration(desiredDuration)


#link = "https://www.youtube.com/watch?v=IGQBtbKSVhY"
#ydl_opts = {
#    'format': 'bestvideo+bestaudio/best',
#    'outtmpl': 'test.mp4',
#}
#with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#    ydl.download([link])






#test = VideoFileClip("test.mp4")
#txt =  TextClip(txt="dancing birdie dances all the time this is really rlong text", fontsize=140, color='white')
#txt = txt.set_start(2).set_end(4).set_position('bottom')
#video = CompositeVideoClip([test,txt])
#video.write_videofile("test_withtext.mp4")

if __name__ == "__main__":
    vidFile = "test.mp4"
    comments = ['comment'+str(i) for i in range(1,10)]
    comments[0] = "long comment made of 9 words should be 3secs but where will it even be cut I wonder very much 0123456789"

    add_subtitles(vidFile, "super long title of the video lets see if it will be scaled lets see", ['-aa2', '-ab2', 'ab3', '>>aaaa4'])