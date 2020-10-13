from pytube import YouTube

def progress(stream, chunk, bytes_remaining):
    contentSize = video.filesize
    size = contentSize - bytes_remaining

    print('\r' + '[Download progress]:[%s%s]%.2f%%;' % (
    '█' * int(size*20/contentSize), ' '*(20-int(size*20/contentSize)), float(size/contentSize*100)), end='')


urls = open("video.txt","r")
line = urls.readline().strip("\n")

while line:
    yt = YouTube(line, on_progress_callback=progress)
    for i in yt.streams:
        print(str(i.resolution))
    #video = yt.streams.first()
    #video.download()
    #line = urls.readline().strip("\n")

urls.close()