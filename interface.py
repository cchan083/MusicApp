from tkinter import *
from guifunctions import show_dirs, show_songs, start_audio, start_playback, pause, end, start_loop, get_songs
from tkinter import ttk
import vlc
from converterfunctions import download
import re
import threading
import os
import shutil

#I learned tkinter from https://www.youtube.com/watch?v=TuLxsvK4svQ (Bro code on youtube)


username = os.getenv("USERNAME")
window = Tk()
window.geometry("720x500")
window.title("GUI for Music App")
window.config(background="#3b424d")
icon = PhotoImage(file="capyicon.png")
window.iconphoto(True, icon)
playlist = Label(window,
                 text="Playlists",
                 font=('Arial', 17, 'bold'),
                 fg='white',
                 bg='#3b424d')
playlist.place(x=20,y=20)
vertseparator = Frame(window, bg='white', width=4, height=3000)
vertseparator.place(x=160, y=0)  
stop_button = Button(window, text="Stop", fg="white", bg="#3b424d", font = ("Arial", 13, 'bold'), command = end)
stop_button.place(x=200, y=15)
pause_button = Button(window, text="Pause", fg="white", bg="#3b424d", font = ("Arial", 13, 'bold'), command = pause)
pause_button.place(x=350, y=15)
player = vlc.MediaPlayer()
currentsong = player.get_media()
loop_button = Button(window, text="Loop", fg="white", bg="#3b424d", font = ("Arial", 13, 'bold'), command=lambda: start_loop(currentsong))
loop_button.place(x=500, y=15)


def playlistupdater():
    global directories
    directories = show_dirs()
    return directories
directories = playlistupdater()         


def playlist_button_maker(playlists):
    for i in range(len(playlists)):
        #button made for each directory which contains the songs inside them for playback
        menu = Menu(window, tearoff=0)
        playlist_buttons = Button(window,
                             text=f'{playlists[i]}',
                             fg="white",
                             bg="#3b424d",
                             font=("Arial", 10, "bold"))      
        playlist_buttons.place(x=20, y=80 + (i * 40))
        files = show_songs(playlists[i]) #returns a list of all songs in currently accessed dir
        for n in range(len(files)):
            filepath = rf'C:\Users\{username}\ytmp3\{playlists[i]}\{files[n]}'
            menu.add_command(label=files[n], command=lambda f=filepath: start_audio(f))
            #lambda for arguments in function
        audiopath = playlists[i]
        menu.add_command(label="Play playlist", command=lambda f=audiopath: start_playback(f))
        # seperate command in the button to play all songs sequentially, with a new function
        playlist_buttons.bind("<Button-1>", lambda event, menu=menu: menu.post(event.x_root, event.y_root))
        #binds LEFT MOUSE BTN to the event so when pressed function is called, whether it be playing a song or playlist

def playlist_status():
        playlist_button_maker(directories)
playlist_status()


actions = ttk.Notebook(window) 
#tabs for adding new songs, playlists and moving songs to playlists

add = Frame(actions, bg="#3b424d", width=500, height= 370)
new_playlist = Frame(actions, bg='#3b424d', width=500, height= 370)
add_to_playlist = Frame(actions, bg='#3b424d', width=500, height= 370)

actions.add(add, text='Add')
actions.add(new_playlist, text='New playlist')
actions.add(add_to_playlist, text='Add to playlist')
style = ttk.Style()
style.configure('TNotebook.Tab', padding=(35, 5), font=('Arial', 10, 'bold'), foreground="#3b424d", background="grey", )
url_entry = Entry(add, font = ('Arial',15))
url_entry.place(x=110, y=140)
playlist_name = Entry(new_playlist, font=('Arial', 15))
playlist_name.place(x=110, y=140)
#styling of tabs and sizing

def url_valid():
    url = url_entry.get()
    linkpattern = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|shorts/|playlist\?list=)?([^&=%\?]{11})'
    #youtube regex matching the url the user types in the entry inside the add tab (https://stackoverflow.com/questions/19377262/regex-for-youtube-url)
    if re.match(linkpattern, url):
        print('correct')
        convert.config(bg='green')
        add.after(3000, lambda: convert.config(bg="white"))
        threading.Thread(target=download, args=(url,)).start()
        refreshingsongs()
        listofsongs(songs)
        # green valid
    else:
        print("false")
        convert.config(bg='red')
        add.after(3000, lambda: convert.config(bg="white"))
        #red if invalid
    url_entry.delete(0, END)
    #delete entry for user convenience after add  convert is pressed
convert= Button(add, text='Convert', command=url_valid)

def newplaylist(name): 
    global directories 
    vname = rf"C:\Users\{username}\ytmp3\{name}"
    if len(directories) < 7:
        add.config(bg='green')
        os.makedirs(vname)
        playlist_name.delete(0, END)
        playlistupdater()
        playlist_status()
        updateplayliststab()
    else:
        add.config(bg='red')
        print("Playlists are full")
# newplaylist() makes a directory from the entry1 entry box, deleted after for user convenience

add = Button(new_playlist, text = "Add playlist", command=lambda: newplaylist(playlist_name.get()))
add.place(x=340, y=141)
convert.place(x=340, y=141)
actions.place(x=180, y=60)


def refreshingsongs():
    global songs
    songs = get_songs()
    #window.after(3000, refreshingsongs)
    return songs              # Update the global `songs` variable

songs = refreshingsongs()
def listofsongs(songs):
    for i in range(len(songs)):
        playlistsbuttons = Button(add_to_playlist,
                             text=f'{songs[i]}',
                             fg="white",
                             bg="#3b424d",
                             font=("Arial", 10, "bold"),
                             width = 20,
                             command=lambda song=songs[i]: selectsong(song))   
        playlistsbuttons.place(x=20, y=80 + (i * 40))
        #makes buttons for all songs in the ytmp3 dir, while assigning the selectsong function for it;s command
def refreshinglist():
    listofsongs(songs)
    window.after(3000, refreshinglist)
refreshinglist()
#refreshes the songs button list every 4 seconds

def playlistbuttons(playlists):
      for i in range(len(playlists)):
        playlists_buttons = Button(add_to_playlist,
                             text=f'{playlists[i]}',
                             fg="white",
                             bg="#3b424d",
                             font=("Arial", 10, "bold"),
                             command=lambda d=playlists[i]: selectplaylist(d))   
        playlists_buttons.place(x=400, y=80 + (i * 40))
def updateplayliststab():
        global directories
        directories = show_dirs()
        playlistbuttons(directories)
        
#same logic as outer playlist buttons, refreshing to match live playlist statuses every 4 sec        
directories = updateplayliststab()

directories = show_dirs()
updateplayliststab()
moving = [] #empty list as a song will get added to it, then a playlist
def selectsong(button):
    global moving
    moving.insert(0, button) #song takes 0 index first
    return moving

def selectplaylist(button):
    global moving
    if len(moving) > 1:
        moving[1] = button  
    else:
        moving.append(button)  #playlist takes 1 index, second
    return moving

def add_playlist():
    global moving
    if len(moving) < 2:
        print("Please select both a song and a playlist.")
        return

    file = moving[0]  # the selected song
    playlist = moving[1]  #the selected playlist

    try:
        # valid path check
        shutil.move(file, playlist)
        print(f"Moved {file} to {playlist}")
        playlist_button_maker(directories)
        moving.clear()  # clear after file moved

    except FileNotFoundError: 
        print("File not found")
move = Button(add_to_playlist, text="Move song", fg="white",
                             bg="#3b424d", 
                             font=("Arial", 10, "bold"), command=lambda: add_playlist())
#after song and playlist is selected, Move song button pressed calls add() function which moves
info = Label(add_to_playlist, bg = "#3b424d", text="Select song first, then playlist to move to", fg='white', font=("Arial", 10, 'bold'), width=40 )
info.place(x=180, y=20)
move.place(x=100, y=20)

window.mainloop()


