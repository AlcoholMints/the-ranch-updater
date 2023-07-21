# I think i need to add data grabber to this and consolidate files

import os
import spotipy
from dotenv import load_dotenv
import requests
sp = spotipy.Spotify()



track_ids = []
for song in song_list:
    artist, track = song.split('-')
    track_id = sp.search(q='artist:' + artist + ' track:' + track, type='track')
    track_ids.append(track_id)
print(track_ids)