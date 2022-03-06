# source ~/.local/lib/python3.6/site-packages/twitch/twitch_env/bin/activate
# Download video info based on vidIDs and the associated messages from TWITCH using its API
# I still need to download the video itself, but I'm currenty using twitch-dl

# UPDATED: ./TwitchDownloaderCLI -m ChatDownload --id 1298807414 -o 1298807414.json
#https://codebeautify.org/json-to-csv


import twitch
import pandas as pd
from collections import Counter
import os
import subprocess
import shutil
import re

#twitch-dl download -q 720p 221837124
#pi0tqjpuaml5cqeg9a8cxyjn89f19l
helix = twitch.Helix('n1lg74ll7q8028d6nz40xpq3sejxic', '1vtkbijcncmfayyt0m9gnlu3ebo5py')

root_path="/media/malahmadi/Samsung USB/TWITCH VIDEOS"
vid_column_name = ['ChannelName', 'TotalFollowers', 'VidID', 'VidTitle', 'CreatedAt','videoViewable', 'VidDuration(minutes)','TotalViews','TotalMsgs','TotalUniqueUserMsgs','Totalmsgs/Duration']
msg_column_name = ['VidID','ChatTimestamp', 'UserName', 'Message']


def hms(s): #convert to seconds
    l = list(map(int, re.split('[hms]', s)[:-1]))
    if len(l) == 3:
        return l[0]*3600 + l[1]*60 + l[2]
    elif len(l) == 2:
        return l[0]*60 + l[1]
    else:
        return l[0]
def moveVid():
    source_dir = os.getcwd()
    target_dir = root_path

    print("Moving the file:",source_dir)
    file_names = os.listdir(source_dir)

    for file_name in file_names:
        if file_name.endswith(".mkv") or file_name.endswith(".mp4"):
            shutil.move(os.path.join(source_dir, file_name), target_dir)

def downloadVid(vidID):
    print("VIDEID",vidID)
    process = subprocess.Popen(['/home/moh/.local/bin/twitch-dl', 'download','-q',' 160p',vidID],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    print(process.stdout.readlines())
    moveVid()


if __name__ == '__main__':
    vid_metadata=[]
    chat_data=[]
    #1286161678
    list_vid=[1271180475]
    for video in helix.videos(list_vid):
        print("Working on: ",video.id)
        #downloadVid(video.id)
        channelName=video.user_name
        totalFollowers=helix.user(video.user_name).followers().total
        videoID=video.id
        videoTitle=video.title
        videoDesc=video.description
        videoCreatedAt=video.created_at
        videoViewable=video.viewable
        videoDuration=hms(video.duration)/60 #we want it in minutes

        videoTotalViews=video.view_count
        comments = video.comments
        tmp_users=[]
        # for i in comments:
        #     print("appending:", i)
        #     chat_data.append((videoID,i.created_at,i.commenter.display_name,i.message.body))
        #     tmp_users.append(i.commenter.display_name)

        TotalUniqueUserMsgs=len((Counter(tmp_users).keys()))
        TotalMsgs=len(tmp_users)

        vid_metadata.append((channelName, totalFollowers, videoID, videoTitle, videoCreatedAt, videoViewable,
                         videoDuration, videoTotalViews, TotalMsgs, TotalUniqueUserMsgs,TotalMsgs/videoDuration))

        vids_df = pd.DataFrame(vid_metadata, columns=vid_column_name)
        csvFile=os.path.join(root_path, "videos_metadata_new_videos.csv")
        vids_df.to_csv(csvFile, index=None)

        chat_df = pd.DataFrame(chat_data, columns=msg_column_name)
        csvFile=os.path.join(root_path, "chats_data_new_videos.csv")
        chat_df.to_csv(csvFile, index=None)

