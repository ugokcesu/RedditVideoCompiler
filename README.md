# RedditVideoCompiler

Python script that creates a compilation of reddit videos from the desired subreddit. Here is an exmaple I uploaded to youtube https://youtu.be/oC31847n9j0


# Guide
Run
```
python driver.py <subreddit name>
```
where subreddit name is one of the subreddits that have video submissions such as "Unexpected", or "DamnThatsInteresting" .
The script will create a folder with the same name as the subreddit and download all needed videos and the  10-minute final.mp4 video which is all videos concatenated.

# Requirements
requirements.txt coming soon.
Besides python libraries, also need to install imagemagic with the "install convert utilities" option

# Features
<li>Adds a random greeting audio recording from the Hello folder to the beginning of the final video.
<li>Adds random backrgound music from the audio folder for videos with no sound.
<li>Censores certain words (profanity) in the comments and titles.
<li>Splits comments to fit screen and adjusts size and speed so they are easily readable.
<li>For changing video options such as minimum upvotes, minimum/maximum duration, modify the call to "filter_submissions" function


![video screenshot](https://github.com/ugokcesu/RedditVideoCompiler/blob/master/redditCapture.JPG)

