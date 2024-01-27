# -*- coding: utf-8 -*-

import os, pytube

# a=webbrowser.get('chrome')

# # Cartella di destinazione
# destination = os.getcwd()
    
# with open("url.txt", "r") as f:
#     stringaUrl=f.read()

# if stringaUrl != '':
#     listaUrl=stringaUrl.split("\n")

#     for url in listaUrl:

#         yt = pytube.YouTube(url)

#         # extract only audio
#         video = yt.streams.filter(only_audio=True).first()

#         # # download the file
#         out_file = video.download(output_path=destination)

#         # save the file
#         base, ext = os.path.splitext(out_file)
#         new_file = base + '.mp3'
#         os.rename(out_file, new_file)
      
#         # result of success
#         print(yt.title + " has been successfully downloaded.")



# import pytube
# url="https://www.youtube.com/watch?v=Ex037JX3-BI&list=PLx5O4Tc4dJBkeDmVAc87mt434HFg9-e0b"
# playlist = pytube.Playlist(url)
# print('Number of videos in playlist: %s' % len(playlist.video_urls))
# playlist.download_all()


# from pytube import Playlist

# url="https://www.youtube.com/watch?v=h0ffIJ7ZO4U&list=PLFw8JYl3SAY7GfEZXekVjN9STaJ7iEoQC"

# play_list = Playlist(url)
# for video in play_list.videos:
#     print("video", video)
#     print(video.streams)
#     video.streams.first().download()



# Cartella di destinazione
destination = os.getcwd()
    


url="https://youtu.be/Q7NjUxGMv7Y?list=RDGMEMQ1dJ7wXfLlqCjwV0xfSNbAVMZZjnfWx0cvw"
# url="https://www.youtube.com/playlist?list=PLx5O4Tc4dJBkHt72pHxFt0sTVILDd9MHf"

yt = pytube.YouTube(url)

# extract only audio
# video = yt.streams.filter(only_audio=True).first()
video = yt.streams.first()

# # download the file
out_file = video.download(output_path=destination)

# save the file
base, ext = os.path.splitext(out_file)
new_file = base + '.mp4'
os.rename(out_file, new_file)
  
# result of success
print(yt.title + " has been successfully downloaded.")





