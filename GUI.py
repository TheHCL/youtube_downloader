import tkinter as tk
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import os
import time
import threading


def check_name(name):
    for i in bad_chars:
        name = name.replace(i,' ')
    return name

# The progress function shows the progress bar while downloading the video
def progress(stream, chunk, bytes_remaining):
    contentSize = stream.filesize
    size = contentSize - bytes_remaining

    print_to_gui('\r' + '[Download progress]:[%s%s]%.2f%%;' % (
    '█' * int(size*20/contentSize), ' '*(20-int(size*20/contentSize)), float(size/contentSize*100)))


def fhd_mp4(url,nv):   # download Full HD video on youtube
    os.chdir(mp4_loc)
    start1 = time.time()
    lock.acquire()
    yt = YouTube(url,on_progress_callback=progress) #url
    current_title.config(text=yt.title)
    window.update()
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
        print_to_gui("No video resolution for 1080p.")
        os.remove(temp_mp3)
        return None
    video = full_hd.first()
    print_to_gui("Download Full HD Video.")
    start_d = time.time()
    video.download(filename="temptemp")  # 1080p mp4 download
    end1 = time.time()
    print_to_gui("Download complete\n")
    #=============================================================#
    os.rename("temptemp.mp4",temp_mp4)
    print_to_gui("Converting files.")
    start2 = time.time()
    if nv=="y":
        os.system("ffmpeg -loglevel quiet -hwaccel cuvid -i temp.mp4 -i temp.mp3 -map 0:v -map 1:a -c:v h264_nvenc -c:a ac3 -b:v 12M output.mp4")
    if nv=="n":
        os.system("ffmpeg -loglevel quiet -i temp.mp4 -i temp.mp3 -map 0:v -map 1:a -c:v h264 -c:a ac3 -s 1920x1080 output.mp4")
    #=============================================================#
    os.remove(temp_mp4)
    os.remove(temp_mp3)
    os.rename("output.mp4",name)
    lock.release()
    end2 = time.time()
    print_to_gui("Convert Done.")
    print_to_gui("\n\n\n1080P video downlaod time : "+str(round((end1-start_d),2))+"secs.\n")
    print_to_gui("Compliation : "+str(round((end2-start2),2))+"secs.\n")
    print_to_gui("Total time : "+str(round((end2-start1),2))+"secs.")
    


def uhd_mp4(url,nv):
    start1=time.time()
    os.chdir(mp4_loc)
    lock.acquire()
    yt = YouTube(url,on_progress_callback=progress) #url
    current_title.config(text=yt.title)
    window.update()
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
        print_to_gui("No video resolution for 4k.")
        os.remove(temp_mp3)
        return None
    video = uhd.first()
    print_to_gui("Download 4k video")
    start_d = time.time()
    video.download(filename="temptemp")  # 2160P webm download
    end1=time.time()
    print_to_gui("Download complete\n")
    print_to_gui("================================\n"+ str(end1-start1))
    #=======================================================#
    os.rename("temptemp.webm","temp.webm")
    print_to_gui("rename OK\n\n\n\n\n\n")
    start2= time.time()
    if nv=="y":   #ffmpeg for NV or not
        os.system("ffmpeg -loglevel quiet -hwaccel cuvid -i temp.webm -i temp.mp3 -map 0:v -map 1:a -c:v h264_nvenc -c:a ac3 -b:v 32M output.mp4") 
    if nv=="n":
        os.system("ffmpeg -loglevel quiet -i temp.webm -i temp.mp3 -map 0:v -map 1:a -c:v h264 -c:a ac3 -s 3840x2160 output.mp4") #cpu 
    os.rename("output.mp4",name)
    os.remove("temp.webm")
    print_to_gui("Convert Done.")
    #======================================================================#
    os.remove(temp_mp3)
    lock.release()
    end2= time.time()
    print_to_gui("\n\n\n4K video downlaod time : "+str(round((end1-start_d),2))+"secs.\n")
    print_to_gui("Compliation : "+str(round((end2-start2),2))+"secs.\n")
    print_to_gui("Total time : "+str(round((end2-start1),2))+"secs.")

def get_text():
    result = url_box.get("1.0",tk.END+"-1c")
    if result != "" or " ":
        youtube_list.insert(1,result)
        url_box.delete("1.0","end")

#https://www.youtube.com/watch?v=bmmtumVQgrg
def del_list_all_text():
    youtube_list.delete(0,tk.END)

def del_list_text():
    youtube_list.delete(youtube_list.curselection())

def initial():
    if nv_acc.get() == True:
        nv = "y"
    if nv_acc.get() == False:
        nv = "n"
    all_items = youtube_list.get(0,"end")
    for i in all_items:
        url = i
        if uhd_var.get() == True:
            #uhd_mp4(url,nv)
            threading.Thread(target=uhd_mp4,args=(url,nv)).start()
        if uhd_var.get() == False:
            #fhd_mp4(url,nv)
            threading.Thread(target=fhd_mp4,args=(url,nv)).start()
        
def print_to_gui(text_string):
    status.config(text=text_string)
    # Force the GUI to update
    window.update()
    
    
    
lock = threading.Lock()

locate = os.getcwd()
temp = locate+"\\temp"
mp4_loc = locate+"\\mp4"
bad_chars = ['<','>',':','"','/','|','?','*',"!"]

dir_path= os.getcwd()+"\\mp4"
url_path = os.getcwd()+"\\URL.txt"
if os.path.exists(dir_path):
    window = tk.Tk()
    #top_frame = tk.Frame(window)
    window.title('Youtube Downloader')
    window.geometry('800x600')
    window.configure(background = '#F0F0F0')
    youtube_list = tk.Listbox(window,selectmode =tk.BROWSE,width=50,height = "10")
    youtube_list.place(x=0,y=0,anchor="nw")
    url_box = tk.Text(window,width=50,height=0.5)
    url_box.place(x=325,y=0,anchor="nw")
    add_btn = tk.Button(window,text = "add",command=get_text)
    add_btn.place(x=325,y=20,anchor="nw")
    del_btn = tk.Button(window,text = "del",command=del_list_text)
    del_btn.place(x=360,y=20,anchor="nw")
    del_all_btn = tk.Button(window,text = "del all",command=del_list_all_text)
    del_all_btn.place(x=395,y=20,anchor="nw")
    start_btn = tk.Button(window,text = "start",command=initial)
    start_btn.place(x=450,y=20,anchor="nw")
    nv_acc = tk.BooleanVar() 
    nv_acc.set(False)
    nv_chkbox = tk.Checkbutton(window, text='NV_acc', var=nv_acc) 
    nv_chkbox.place(x=325,y=50)
    uhd_var = tk.BooleanVar() 
    uhd_var.set(False)
    uhd_chkbox = tk.Checkbutton(window, text='UHD', var=uhd_var) 
    uhd_chkbox.place(x=325,y=75)
    current_title = tk.Label(window)
    current_title.place(x=0,y=180)
    status = tk.Label(window)
    status.place(x=0,y=200)
    window.mainloop()
    
    

else:
    print("Directory Created.\nPlease re-run the script.")
    os.mkdir(dir_path)






    

