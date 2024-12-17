import yt_dlp
import os 
import vlc
import time


def download(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(title)s.mid',
    }# downloads best audio as mp3
    
    with yt_dlp.YoutubeDL(ydl_opts) as mp3:
        mp3.download([video_url])
def filepath(playlist):
    filepath = None
    while filepath == None:
        filesinplaylist = os.listdir(playlist)
        for index, files in enumerate(filesinplaylist):
            print(index, files)
        #prints index of songs in list
        choice = int(input("What song? (number for choice): "))
        directory = rf'{playlist}'
        length = len(filesinplaylist) - 1
        print(length)
        try:
            filepath = os.path.join(directory, filesinplaylist[choice])
            #calls an item in the list and returns
            break
        except:
            print("Choice is out of range")
            filepath = None
            continue
    return filepath
        
            
   
            
    

def actionswhenplaying():
     actions = input("""
pause/play (p)
kill stream / exit
""")
     return actions



def play_audio(audio_path):
    player = vlc.MediaPlayer(audio_path)
    time.sleep(1)
    player.play()
    print(player.is_playing())
    actions = ""
    while actions != "kill stream":
        actions = actionswhenplaying()
        if actions == "p":
            player.pause()
        #pause if 'p'
        elif actions == "exit":
            player.stop()
    player.stop()
    
def getactions():
    user = input("""
    add
    new playlist
    add to playlist
    play
    done
    """)
    return user
            

    
    


