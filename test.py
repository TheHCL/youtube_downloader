from pytube import YouTube
from moviepy.editor import *
import os
import ffmpeg

locate = os.getcwd()
temp = locate+"\\temp"
mp4_loc = locate+"\\mp4"



# The progress function shows the progress bar while downloading the video
def progress(stream, chunk, bytes_remaining):
    contentSize = video.filesize
    size = contentSize - bytes_remaining

    print('\r' + '[Download progress]:[%s%s]%.2f%%;' % (
    '█' * int(size*20/contentSize), ' '*(20-int(size*20/contentSize)), float(size/contentSize*100)), end='')

def fhd_mp4():   # download Full HD video on youtube
    os.chdir(temp)
    url = "https://www.youtube.com/watch?v=TvWcU3aztmo"
    yt = YouTube(url)
    temp_mp4 = yt.title+".mp4"
    temp_mp3 = yt.title +".mp3"
    video=yt.streams.first()
    video.download()  #360p mp4 download
    mp4_360P = VideoFileClip(temp_mp4)
    mp4_360P.audio.write_audiofile(temp_mp3)  # change the 360p mp4 file to mp3 
    mp4_360P.close()
    os.remove(temp_mp4) # now we have the mp3 file only
    os.chdir(mp4_loc)
    full_hd = yt.streams.filter(res="1080p",type="video",file_extension="mp4")
    video = full_hd.first()
    video.download()  # 1080p mp4 download
    videoclip = VideoFileClip(temp_mp4)
    audioclip = AudioFileClip(temp+"\\"+temp_mp3)
    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    videoclip.write_videofile("new.mp4")
    videoclip.close()
    os.remove(temp_mp4)
    os.remove(temp+"\\"+temp_mp3)
    os.rename("new.mp4","[FHD]"+temp_mp4)

def uhd_mp4():
    os.chdir(temp)
    url = "https://www.youtube.com/watch?v=TvWcU3aztmo"
    yt = YouTube(url)
    temp_mp4 = yt.title+".mp4"
    temp_mp3 = yt.title +".mp3"
    video=yt.streams.first()
    video.download()  #360p mp4 download
    mp4_360P = VideoFileClip(temp_mp4)
    mp4_360P.audio.write_audiofile(temp_mp3)  # change the 360p mp4 file to mp3 
    mp4_360P.close()
    os.remove(temp_mp4) # now we have the mp3 file only
    os.chdir(mp4_loc)
    uhd = yt.streams.filter(res="2160p",type="video",file_extension="webm")
    video = uhd.first()
    print("Download 4k video")
    video.download()  # 2160P webm download
    print("Download complete")
    #=======================================================#
    os.rename(yt.title+".webm","old.webm")
    print("rename OK")
    os.system("ffmpeg -i old.webm -c copy output.mp4")
    os.rename("output.mp4",temp_mp4)
    os.remove("old.webm")
    print("Convert Done.")
    #====================================================================#
    videoclip = VideoFileClip(temp_mp4)
    audioclip = AudioFileClip(temp+"\\"+temp_mp3)
    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    print("writing audio")
    videoclip.write_videofile("new.mp4")
    print("write done")
    #videoclip.close()
    #os.remove(temp_mp4)
    #os.remove(temp+"\\"+temp_mp3)
    #os.rename("new.mp4","[UHD]"+temp_mp4)


uhd_mp4()

#fhd_mp4()

#url = "https://www.youtube.com/watch?v=TvWcU3aztmo"

#yt = YouTube(url, on_progress_callback=progress)

#fil= yt.streams.filter(res="2160p",type="video",file_extension="webm")
#video = fil.first()
#video.download()



