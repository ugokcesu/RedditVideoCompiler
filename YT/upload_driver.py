import os
import subprocess
from os import path
import sys

def create_arguments(file, title, description, keywords):
    options = '--file "' + file + '"'
    options += ' --title "' + title + '"'
    options += ' --description "' + description + '"'
    options += ' --keywords "' + keywords + '"'
    return options

def upload_video(options):
    os.system("python YT/upload_video.py " + options)
    #subprocess.run(["python.exe YT/upload_video.py ", options])

def auto_arguments(subName):
    file = path.join(r"C:\VSCode\REDDITCOMPILER", subName, "final.mp4")
    title = "Reddit's best r/" + subName + " videos compilation with funniest comments"
    description = "A compilation of Reddit's best r/subName videos with the best comments!\n \
        #Reddit #videos" 
    keywords = subName + ", reddit, videos, memes"
    return create_arguments( file, title, description, keywords)

    

if __name__ == "__main__":
    args = auto_arguments(sys.argv[1])
    upload_video(args)

