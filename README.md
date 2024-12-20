# Libraries I used

```tkinter```: Used for the GUI 

```vlc```: for media playback

```re``` (regular expressions): for client-side youtube format validation

```threading```: allowing concurrent execution for downloading and playing music simultaneously

```os``: making new playlists

```shutil```: moving music into playlists

## GUI looks like this: 

![gui png](gui.png)


## Setting up the layout for my GUI

```username = os.getenv("USERNAME")
window = Tk()
player = vlc.MediaPlayer()

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

currentsong = player.get_media()
loop_button = Button(window, text="Loop", fg="white", bg="#3b424d", font = ("Arial", 13, 'bold'), command=lambda: start_loop(currentsong))
loop_button.place(x=500, y=15)
```

Here, I initialised the window and player for the app, while also choosing the window size as ```"720x500"```, setting the title

- Used the ```Frame()``` for the separator
- Setup all the buttons, including Stop, Pause, Loop, 

## Updatating the playlists buttons

```
def playlistupdater():
    global directories
    directories = show_dirs()
    return directories
directories = playlistupdater()  
```
show_dirs(): 

```
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
```
returns a list of files which are not called ```.venv``` and ```__pycache__```


## Making the playlist buttons

```
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
```
This adds new buttons while simultaneously creating menu buttons inside, containing the media files inside, which play when clicked

## Creation of the 3 buttons (Add, New playlist, Add to playlist)
```
actions = ttk.Notebook(window) 
#tabs for adding new songs, playlists and moving songs to playlists

add = Frame(actions, bg="#3b424d", width=500, height= 370)
new_playlist = Frame(actions, bg='#3b424d', width=500, height= 370)
add_to_playlist = Frame(actions, bg='#3b424d', width=500, height= 370)

actions.add(add, text='Add')
actions.add(new_playlist, text='New playlist')
actions.add(add_to_playlist, text='Add to playlist')
```
- Adding the buttons to the window Notebook

### Styling of the notebook buttons
```
style = ttk.Style()
style.configure('TNotebook.Tab', padding=(35, 5), font=('Arial', 10, 'bold'), foreground="#3b424d", background="grey", )
url_entry = Entry(add, font = ('Arial',15))
url_entry.place(x=110, y=140)
playlist_name = Entry(new_playlist, font=('Arial', 15))
playlist_name.place(x=110, y=140)
#styling of tabs and sizing
```

## Adding the converter 
```
ef url_valid():
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
```

- Regex is from stackoverflow for client side checking
- If URL matches pattern, button turns green, if not it turns red

## Making new playlists

```
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
```
- maxmimum playlist amount is 7
- After adding a playlist, the buttons are recreated to ensure real-time creation of playlists and buttons
- I first went for a window.after() approach to update indefinitely every 3 seconds, but it was not optimised and could not stay open for extended periods of time.

## Allowing newly downloaded songs to show real time in the add to playlist tab

```
def refreshingsongs():
    global songs
    songs = get_songs()
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
```
- After being downloaded, a button is made in the add_to_playlist tab, allowing the song to be moved to a playlist

