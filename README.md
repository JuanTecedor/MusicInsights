# Music Insights

This application downloads all your liked Spotify songs and stores them in three json files:
- songs.json. Each song has the following fields:
    - Time when it was added.
    - Artists.
    - Duration in milliseconds.
    - Explicit.
    - ID.
    - Name.
    - Popularity.
    - Track number.
    - Is local.
    - Album ID.
    - Disc number.
    - Song type (currently unused).
- artists.json. Each artist has the following fields:
  - Name.
  - ID.
  - Artist type (currently unused).
- albums.json. Each album has the following fields:
  - Album type.
  - Artists.
  - ID.
  - Name.
  - Release date.
  - Release date precision.
  - Songs.
  - Total tracks.

It additionaly shows some statistics like number of songs, albums and artists.

## How to run:
Requirements:
```
$ python3 --version
Python 3.11.1
```

```
pip install -r requirements.txt
```

Run with:
```
python3 src/main.py
```
or with:
```
python3 src/main.py --download_and_save_library
```

NEW:
python3.11 -m venv ./.venv
source .venv/bin/activate
pip install -r requirements.txt
