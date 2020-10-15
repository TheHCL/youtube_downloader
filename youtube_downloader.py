from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import os
import time

locate = os.getcwd()
temp = locate+"\\temp"
mp4_loc = locate+"\\mp4"
bad_chars = ['<','>',':','"','/','|','?','*',"!"]

def check_name(name):
    for i in bad_chars:
        name = name.replace(i,' ')
    return name

# The progress function shows the progress bar while downloading the video
def progress(stream, chunk, bytes_remaining):
    contentSize = stream.filesize
    size = contentSize - bytes_remaining

    print('\r' + '[Download progress]:[%s%s]%.2f%%;' % (
    '█' * int(size*20/contentSize), ' '*(20-int(size*20/contentSize)), float(size/contentSize*100)), end='')

def fhd_mp4(url):   # download Full HD video on youtube
    os.chdir(mp4_loc)
    yt = YouTube(url,on_progress_callback=progress) #url
    name = "[FHD]"+yt.title+".mp4"
    name = check_name(name)
    temp_mp4 = "temp.mp4"
    temp_mp3 = "temp.mp3"
    video=yt.streams.first()
    video.download(filename="temptemp")  #360p mp4 download
    os.rename("temptemp.mp4",temp_mp4)
    mp4_360P = VideoFileClip(temp_mp4)
    mp4_360P.audio.write_audiofile(temp_mp3)  # change the 360p mp4 file to mp3 
    mp4_360P.close()
    os.remove(temp_mp4) # now we have the mp3 file only
    full_hd = yt.streams.filter(res="1080p",type="video",file_extension="mp4")
    if str(full_hd)=="[]":
        print("No video resolution for 1080p.")
        os.remove(temp_mp3)
        return None
    video = full_hd.first()
    print("Download Full HD Video.")
    video.download(filename="temptemp")  # 1080p mp4 download
    print("Download complete\n")
    #=============================================================#
    os.rename("temptemp.mp4",temp_mp4)
    print("Converting files.")
    os.system("ffmpeg -i temp.mp4 -i temp.mp3 -map 0:v -map 1:a -c:v h264 -c:a ac3 -s 1920x1080 output.mp4")
    #=============================================================#
    os.remove(temp_mp4)
    os.remove(temp_mp3)
    os.rename("output.mp4",name)
    print("Convert Done.")


def uhd_mp4(url):
    start1=time.time()
    os.chdir(mp4_loc)
    yt = YouTube(url,on_progress_callback=progress) #url
    name = "[UHD]"+yt.title+".mp4"
    name = check_name(name)
    temp_mp4 = "temp.mp4"
    temp_mp3 = "temp.mp3"
    video=yt.streams.first()
    video.download(filename="temptemp")  #360p mp4 download
    os.rename("temptemp.mp4",temp_mp4)
    mp4_360P = VideoFileClip(temp_mp4)
    mp4_360P.audio.write_audiofile(temp_mp3)  # change the 360p mp4 file to mp3 
    mp4_360P.close()
    os.remove(temp_mp4) # now we have the mp3 file only
    uhd = yt.streams.filter(res="2160p",type="video",file_extension="webm")
    if str(uhd)=="[]":
        print("No video resolution for 4k.")
        os.remove(temp_mp3)
        return None
    video = uhd.first()
    print("Download 4k video")
    video.download(filename="temptemp")  # 2160P webm download
    end1=time.time()
    print("Download complete\n")
    print("================================\n"+ str(end1-start1))
    #=======================================================#
    os.rename("temptemp.webm","temp.webm")
    print("rename OK\n\n\n\n\n\n")
    start2= time.time()
    os.system("ffmpeg -i temp.webm -i temp.mp3 -map 0:v -map 1:a -c:v h264 -c:a ac3 -s 3840x2160 output.mp4")
    #ffmpeg -hwaccel cuvid -c:v h264_cuvid -i 0.mp4 -c:v h264_nvenc -y 00.mp4
    os.rename("output.mp4",name)
    os.remove("temp.webm")
    print("Convert Done.")
    #======================================================================#
    os.remove(temp_mp3)
    end2= time.time()
    print("Compliation : "+str(end2-start2)+"secs.")





dir_path= os.getcwd()+"\\mp4"
if os.path.exists(dir_path):
    url = input("Please input URL:\t")
    res = input("1.FHD(1920*1080) 2.UHD(3840*2160):\t")
    if res =="1":
        fhd_mp4(url)
    if res =="2":
        uhd_mp4(url)
    
else:
    print("Directory Created.\nPlease re-run the script.")
    os.mkdir(dir_path)





