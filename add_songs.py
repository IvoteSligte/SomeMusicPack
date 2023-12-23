import requests
from pytube import Playlist
import os
import hashlib
from moviepy.editor import VideoFileClip
import soundfile as sf
import pyloudnorm as pyln

def unicode_to_ascii_hash(input_string):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(input_string.encode('utf-8'))
    hash_result = hash_algorithm.hexdigest()
    return hash_result

def convert_mp4_to_mp3(input_file, output_file):
    video = VideoFileClip(input_file)
    video.audio.write_audiofile(output_file, codec="mp3")

directory = "plugins/Custom Songs"
playlist_url = "https://youtube.com/playlist?list=PLSX27Q9iirpV8z3Ed0kl3I-ThxrEWI538&si=tU7nM_fiEvSvA6IJ"

song_files = set()

playlist = Playlist(playlist_url)
for yt in playlist.videos:
    print("Downloading ", yt.title)
    filename = unicode_to_ascii_hash(yt.title)
    filename = filename.replace("/", ".")
    song_files.add(filename)
    path = os.path.join(directory, filename) + ".mp3"

    if os.path.isfile(path):
        continue

    video = yt.streams.filter(only_audio = False, only_video = False).first()
    freshDownload = video.download(directory)
    convert_mp4_to_mp3(freshDownload, path)
    os.remove(freshDownload)

    # https://medium.com/@poudelnipriyanka/audio-normalization-9dbcedfefcc0
    data, rate = sf.read(path)
    peak_normalized_audio = pyln.normalize.peak(data, -1.0)
    meter = pyln.Meter(rate)
    loudness = meter.integrated_loudness(data)
    loudness_normalized_audio = pyln.normalize.loudness(data, loudness, -12.0)
    sf.write(path, loudness_normalized_audio, rate)

