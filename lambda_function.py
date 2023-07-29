
# import libraries
import requests
import os
from get_spotify_track_uris import convert_to_spotify_track_uris, chunkify
from playlist_cleaner import playlist_cleaner
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def lambda_handler():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope = "playlist-modify-public",
    client_id = os.getenv('CLIENT_ID'),
    client_secret = os.getenv('CLIENT_SECRET'),
    redirect_uri = os.getenv('REDIRECT_URI'),
    ))
    playlist_id = os.getenv('YOUR_PLAYLIST_ID')
    spotify_track_uris = convert_to_spotify_track_uris()
    playlist_cleaner()  # deletes duplicates and old songs on existing playlist

    if len(spotify_track_uris) > 100:
        spotify_track_uris = chunkify(spotify_track_uris)
        for chunk in spotify_track_uris:
            add_songs_to_playlist(playlist_id, chunk)
    else:
        add_songs_to_playlist(playlist_id, spotify_track_uris)

def add_songs_to_playlist(playlist_id, track_uris):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope = "playlist-modify-public",
    client_id = os.getenv('CLIENT_ID'),
    client_secret = os.getenv('CLIENT_SECRET'),
    redirect_uri = os.getenv('REDIRECT_URI'),
    ))
    results = sp.playlist_add_items(playlist_id, track_uris)
    
    if 'snapshot_id' in results:
        print("Songs added to the playlist successfully!")
    else:
        print("Failed to add the songs to the playlist.")

if __name__ == "__main__":
    lambda_handler()