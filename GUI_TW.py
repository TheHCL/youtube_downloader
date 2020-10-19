from pytube import YouTube,Playlist
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import os
import time
import tkinter as tk
import threading
import re
from tkinter import messagebox



def check_name(name):
    for i in bad_chars:
        name = name.replace(i,'')
    return name

def del_from_list(url):
    label =url
    idx = youtube_list.get(0, tk.END).index(label)
    youtube_list.delete(idx)
    window.update()


def progress(stream, chunk, bytes_remaining):
    contentSize = stream.filesize
    size = contentSize - bytes_remaining

    print_to_gui('\r' + '[下載進度]:[%s%s]%.2f%%;' % (
    '█' * int(size*20/contentSize), ' '*(20-int(size*20/contentSize)), float(size/contentSize*100)))


def yt2mp3(url,nv):
    os.chdir(mp3_loc)
    lock.acquire()
    global count
    global count_err
    global list_all
    try:
        yt = YouTube(url,on_progress_callback=progress)
        name = check_name(yt.title)
        name+=".mp3"
        mp4_ori=yt.streams.filter(type="audio",file_extension="mp4") # mp4 audio
        video=mp4_ori.first()
        if str(video)=="[]":
            print_to_gui("沒有MP3檔可下載")
            return None
        video.download(filename="temptemp")
        if nv=="y":
            os.system("ffmpeg -hwaccel cuvid -i temptemp.mp4 -vn -acodec libmp3lame -q:a 0 temp.mp3")
        if nv=="n":
            os.system("ffmpeg -i temptemp.mp4 -vn -acodec libmp3lame -q:a 0 temp.mp3")
        os.remove("temptemp.mp4")
        os.rename("temp.mp3",name)
        del_from_list(url)
        lock.release()
        print_to_gui(name+"\t下載完成")
        count+=1
        time.sleep(5)
    except:
        del_from_list(url)
        lock.release()
        print_to_gui("無法下載的音樂檔")
        count_err+=1
        pass
    if list_all==(count+count_err):
        window.title('全數下載完成'+"  [成功]:"+str(count)+"[失敗]:"+str(count_err))
        status.config(text="已全數下載完成"+"  [成功]:"+str(count)+"[失敗]:"+str(count_err))
    else :
        window.title('Youtube Downloader'+"  [成功]:"+str(count)+"[失敗]:"+str(count_err))


def fhd_mp4(url,nv):   # download Full HD video on youtube
    os.chdir(mp4_loc)
    lock.acquire()
    global count
    global count_err
    global list_all
    try:
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
            print_to_gui("沒有1080P影片檔可下載")
            time.sleep(2)
            print_to_gui("嘗試下載480P影片檔")
            f480 = yt.streams.filter(res="480p",type="video",file_extension="mp4")
            if str(f480)=="[]":
                print_to_gui("沒有480P影片檔可下載")
                time.sleep(2)
                print_to_gui("嘗試下載360P影片檔")
                video=yt.streams.first()
                print_to_gui("下載360P影片檔")
                name = "[360P]"+yt.title+".mp4"
                name = check_name(name)
            else:
                video =f480.first()
                print_to_gui("下載480P影片檔")
                name = "[480P]"+yt.title+".mp4"
                name = check_name(name)
        else:    
            video = full_hd.first()
            print_to_gui("下載Full HD 影片中")
        
        video.download(filename="temptemp")  # 1080p mp4 download
        
        
        #=============================================================#
        os.rename("temptemp.mp4",temp_mp4)
        print_to_gui("轉檔中.")
        
        if nv=="y":
            os.system("ffmpeg -hwaccel cuvid -i temp.mp4 -i temp.mp3 -map 0:v -map 1:a -c:v h264_nvenc -c:a ac3 -b:v 12M output.mp4")
        if nv=="n":
            os.system("ffmpeg -i temp.mp4 -i temp.mp3 -map 0:v -map 1:a -c:v h264 -c:a ac3 -s 1920x1080 output.mp4")
        #=============================================================#
        os.remove(temp_mp4)
        os.remove(temp_mp3)
        os.rename("output.mp4",name)
        
        lock.release()
        
        print_to_gui(name+"\t下載完成")
        count+=1
        time.sleep(5)
    except:
        del_from_list(url)
        lock.release()
        print_to_gui("無法下載的影片檔")
        count_err+=1
        pass
    if list_all==(count+count_err):
        window.title('全數下載完成'+"  [成功]:"+str(count)+"[失敗]:"+str(count_err))
        status.config(text="已全數下載完成"+"  [成功]:"+str(count)+"[失敗]:"+str(count_err))
    else :
        window.title('Youtube Downloader'+"  [成功]:"+str(count)+"[失敗]:"+str(count_err))

def uhd_mp4(url,nv):
    start1=time.time()
    os.chdir(mp4_loc)
    lock.acquire()
    global count
    global count_err
    global list_all
    try:
        yt = YouTube(url,on_progress_callback=progress) #url
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
            print_to_gui("沒有4K影片可下載.")
            os.remove(temp_mp3)
            return None
        video = uhd.first()
        print_to_gui("4K影片下載中")
        start_d = time.time()
        video.download(filename="temptemp")  # 2160P webm download
        end1=time.time()
        print_to_gui("4K影片下載完成")
        #=======================================================#
        os.rename("temptemp.webm","temp.webm")
        start2= time.time()
        if nv=="y":   #ffmpeg for NV or not
            os.system("ffmpeg -loglevel quiet -hwaccel cuvid -i temp.webm -i temp.mp3 -map 0:v -map 1:a -c:v h264_nvenc -c:a ac3 -b:v 32M output.mp4") 
        if nv=="n":
            os.system("ffmpeg -loglevel quiet -i temp.webm -i temp.mp3 -map 0:v -map 1:a -c:v h264 -c:a ac3 -s 3840x2160 output.mp4") #cpu 
        os.rename("output.mp4",name)
        os.remove("temp.webm")
        print_to_gui("轉檔完成.")
        #======================================================================#
        os.remove(temp_mp3)
        lock.release()
        end2= time.time()
        print_to_gui(name+"  總時間 : "+str(round((end2-start1),2))+"secs.")
        count+=1
    except:
        del_from_list(url)
        lock.release()
        print_to_gui("無法下載的影片檔")
        count_err+=1
        pass
    if list_all==(count+count_err):
        window.title('全數下載完成'+"  [成功]:"+str(count)+"[失敗]:"+str(count_err))
        status.config(text="已全數下載完成"+"  [成功]:"+str(count)+"[失敗]:"+str(count_err))
    else :
        window.title('Youtube Downloader'+"  [成功]:"+str(count)+"[失敗]:"+str(count_err))

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

def yt_playlist():
    
    y = youtube_list.get(0,"end")
    youtube_list.delete(0,"end")
    for k in y:
        playlist = Playlist(k)
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    #print(len(playlist.video_urls))
    for x in playlist.video_urls:
        youtube_list.insert(1,x)
    
    window.update()
    
    


def initial():
    status.config(text="")
    global list_all
    list_all = youtube_list.size()
    
    if nv_acc.get() == True:
        nv = "y"
    if nv_acc.get() == False:
        nv = "n"
    if yt_list_var.get() == True:
        yt_playlist()
        list_all = youtube_list.size()
    all_items = youtube_list.get(0,"end")
    for i in all_items:
        url = i
        if res.get() == "UHD":
            threading.Thread(target=uhd_mp4,args=(url,nv)).start()
        if res.get() == "FHD": #mp4 1080p mp3 
            threading.Thread(target=fhd_mp4,args=(url,nv)).start()
        if res.get() == "MP3":
            threading.Thread(target=yt2mp3,args=(url,nv)).start()
def print_to_gui(text_string):
    status.config(text=text_string)
    # Force the GUI to update
    window.update()

def restart_program():
    window.destroy()
    window.quit()
    os.system("GUI_TW.exe")

bad_chars = ['<','>',':','"','/','|','?','*',"!"]
lock = threading.Lock()
locate = os.getcwd()
mp3_loc = locate+"\\mp3"
mp4_loc = locate+"\\mp4"

if os.path.exists(mp3_loc) and os.path.exists(mp4_loc):
    count=0
    count_err =0
    list_all =0
    list_all=0
    window = tk.Tk()
    
    window.title('Youtube Downloader')
    window.geometry('500x525')
    window.configure(background = '#F0F0F0')
    ulb = tk.Label(window,text="請貼上網址")
    ulb.grid(sticky=tk.W)
    url_box = tk.Text(window,width=45,height=0.5)
    url_box.grid(sticky=tk.W)
    ylb = tk.Label(window,text="下載清單")
    ylb.grid(sticky=tk.W)
    youtube_list = tk.Listbox(window,selectmode =tk.BROWSE,width=45)
    youtube_list.grid(sticky=tk.W)
    
    add_btn = tk.Button(window,text = "添加",command=get_text)
    add_btn.grid(column=0,sticky=tk.W)
    del_btn = tk.Button(window,text = "刪除",command=del_list_text)
    del_btn.grid(column=0,sticky=tk.W)
    del_all_btn = tk.Button(window,text = "清空",command=del_list_all_text)
    del_all_btn.grid(column=0,sticky=tk.W)
    restart_btn = tk.Button(window,text = "重啟",command=restart_program)
    restart_btn.grid(column=0,sticky=tk.W)
    yt_list_var = tk.BooleanVar() 
    yt_list_var.set(False)
    yt_list_chkbox = tk.Checkbutton(window, text='播放清單', var=yt_list_var) 
    yt_list_chkbox.grid(column=0,sticky=tk.W)
    res = tk.StringVar()
    res.set('a')
    r1 = tk.Radiobutton(window,text="FHD",variable=res,value ="FHD")
    r2 = tk.Radiobutton(window,text="UHD",variable=res,value ="UHD")
    r3 = tk.Radiobutton(window,text="MP3",variable=res,value ="MP3")
    r1.grid(column=0,sticky=tk.W)
    r2.grid(column=0,sticky=tk.W)
    r3.grid(column=0,sticky=tk.W)
    nv_acc = tk.BooleanVar() 
    nv_acc.set(False)
    nv_chkbox = tk.Checkbutton(window, text='硬體加速', var=nv_acc) 
    nv_chkbox.grid(column=0,sticky=tk.W)
    status = tk.Label(window)
    status.grid(column=0,sticky=tk.W)
    start_btn = tk.Button(window,text = "點我開始",command=initial)
    start_btn.grid(column=0,sticky=tk.W)
    window.mainloop()
    
else :
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Information","目錄已創建.\n請重新執行程式.")
    try:
        os.mkdir(mp3_loc)
        os.mkdir(mp4_loc)
    except:
        if os.path.exists(mp3_loc):
            os.mkdir(mp4_loc)
        if os.path.exists(mp4_loc):
            os.mkdir(mp3_loc)
    