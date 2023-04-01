# Music Insights

## What Does This App Do
* **Downloads all your liked songs from Spotify** and related data and stores it in three files:
    * All the data is stored in human-readable **JSON** files, this serves as a **backup** and for loading the data later on.
    * Data stored for songs (songs.json): Time when it was liked, artists, duration, if it is explicit, ID, name, popularity, track number, if it is local, corresponding album ID and disk number.
    * Data stored for albums (albums.json): Artists, ID, name, release date, release date precision, songs, total tracks, genres, label and popularity.
    * Data stored for artists (artists.json): Artist name, ID, followers, genres and popularity.
* **Creates a playlist for each decade with your liked songs** (I.E.: It groups liked songs by decades). This has the caveat that remastered albums will appear in recent years instead of the original release date.

### Prerequisites

* You need a client_id, for that head over to [https://developer.spotify.com/dashboard/applications](https://developer.spotify.com/dashboard/applications) and create one app. Get the client id.
* Modify music_insights/spotify/credentials.py and add the following line: ```client_id = ...```.
* Add the following redirect URL to the APP settings: ```http://localhost/```.
* Authorize the email from the Spotify user you want to read/write data to.

### Running the App
#### If you are using Docker and VSCode:

* Extension Dev Containers is strongly recommended.
* ```$ docker-compose up --build -d music_insights```
* Attach to Running Container...

#### If you are using a venv:
```
$ cd $PROJECT_ROOT/music_insights
$ python3.11 -m venv ./.venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ python music_insights/main.py --create_playlists_by_decades
```

If you want to debug and run the tests also do:
```
$ pip install -r requirements-dev.txt
```

When downloading data and creating the playlists, the app will ask for authorization, follow the instructions in the terminal.
