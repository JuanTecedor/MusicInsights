# Music Insights

```
(.venv) ➜  MusicInsights git:(main) ✗ python main.py -h
usage: main.py [-h] [-s {api,file}] [-d DIR] [-j] [-c]

options:
  -h, --help            show this help message and exit
  -s {api,file}, --src {api,file}
                        Set the source from which to load the library.
  -d DIR, --dir DIR     Change the origin (when using the file as a source)and destination directory of the library.
  -j, --json            Specifies if the program should save a json file in the output directory.
  -c, --create_playlists
                        Specifies if the program should create playlists by decades.
```

## What Does This App Do
* **Downloads all your liked songs from Spotify** and related data and stores it in three files:
    * All the data is stored in human-readable **JSON** files, this serves as a **backup** and for loading the data later on.
    * Data stored for songs (songs.json): Time when it was liked, artists, duration, if it is explicit, ID, name, popularity, track number, if it is local, corresponding album ID and disk number.
    * Data stored for albums (albums.json): Artists, ID, name, release date, release date precision, songs, total tracks, genres, label and popularity.
    * Data stored for artists (artists.json): Artist name, ID, followers, genres and popularity.
* **Creates a playlist that group your liked songs by decades**: This has the caveat that remastered albums will appear in recent years instead of the original release date.

### Prerequisites

* You need a `client_id`. Go to [https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) and create one app. Copy the client id.
* Modify music_insights/spotify/credentials.py and at the following line: ```client_id = ...``` paste the `client_id`.
* Add the following redirect URL to the APP settings: [http://localhost/](http://localhost/).
* Authorize the email from the Spotify user you want to read/write data to.

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

#### If you are using Docker:

If you are using Docker all the requirements are always installed by default.

To run all the tests and checks (mypy, pytest, flake8, isort, etc):

```docker compose -f docker/compose.yml up --build test```

To run the application with your custom flags:

```docker compose -f docker/compose.yml run --entrypoint "python main.py -h" main```
