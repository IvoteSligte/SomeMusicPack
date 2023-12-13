import requests
from pytube import Playlist
import os

directory = "plugins/Custom Songs"
playlist_url = "https://youtube.com/playlist?list=PLSX27Q9iirpV8z3Ed0kl3I-ThxrEWI538&si=tU7nM_fiEvSvA6IJ"

song_files = set()

playlist = Playlist(playlist_url)
for yt in playlist.videos:
    print("Downloading ", yt.title)
    filename = yt.title.replace("/", ".") + ".mp3"
    song_files.add(filename)

    if os.path.isfile(os.path.join(directory, filename)):
        continue
    
    audio = yt.streams.filter(only_audio = True).first()
    audio.download(directory, filename = filename)

files = os.listdir(directory)
for f in files:
    if f in song_files:
        continue
    
    base, ext = os.path.splitext(f)
    
    if not ext == ".mp3":
        raise ValueError("File does not have a .mp3 extension.")
    
    os.remove(os.path.join(directory, f))



