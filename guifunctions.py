import os 
import vlc
import time
import threading

username = os.getenv("USERNAME")
def show_songs(playlist):
    filepath = rf"C:\Users\{username}\ytmp3\{playlist}"
    print(filepath)
    lst = []
    dirs = os.listdir(filepath)
    print(dirs)
    for i in dirs:
        lst.append(i) 
    return lst
#print(show_songs('test'))
def show_dirs():
    filepath = rf'C:\Users\{username}\ytmp3'
    lst = []
    for entry in os.listdir(filepath):
        full_path = os.path.join(filepath, entry) 
        if os.path.isdir(full_path): 
            fullpath = full_path[32:]
            if (fullpath != ".venv") and (fullpath != "__pycache__") and (fullpath != "build"): #cannot be these 2 as they do not contain music
                lst.append(fullpath) 
    return lst

current_audio = None
player = vlc.MediaPlayer()
def play_audio(audio_path):
    media = vlc.Media(audio_path)
    player.set_media(media)
    if player.is_playing():
        player.stop() 
    player.play()
def start_audio(audio_path):
    threading.Thread(target=play_audio, args=(audio_path,), daemon=True ).start() #threading to stop GUI from 'not responding'
def play_playlist(directory):
    path = rf'C:\Users\{username}\ytmp32\{directory}'
    audio_files = os.listdir(path)
    for i in range(len(audio_files)):
        media = vlc.Media(f"{path}\{audio_files[i]}")
        player.set_media(media)
        player.play()
        while player.get_state() not in [vlc.State.Ended, vlc.State.Error]:
            time.sleep(1)
def start_playback(directory):
    #new thread to stop GUI from crashing
    threading.Thread(target=play_playlist, args=(directory,), daemon=True).start()

def pause():
    player.pause()
def end():
    player.stop()
def loop():
    player.play()
    while True:
        time.sleep(1)  
        state = player.get_state()
        if state == vlc.State.Ended:
            player.stop()  #stop current stream
            player.play()  
def start_loop(song):
    threading.Thread(target=loop, daemon=True).start()

def get_songs():
    filepath = rf'C:\Users\{username}\ytmp3'
    list = []
    allfiles = os.listdir(filepath) 
    for i in allfiles:
        type = i[-4:]
        if type == ".mid":
            list.append(i)
        else:
            continue
    return list
