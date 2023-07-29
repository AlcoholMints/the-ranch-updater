# import libraries
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta
from get_spotify_track_uris import convert_to_spotify_track_uris
from get_spotify_track_uris import chunkify
from dateutil.parser import isoparse

load_dotenv()

def playlist_cleaner():

    # * Initialize Spotipy with necessary scopes and authentication
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope = "playlist-modify-public",
        client_id = os.getenv('CLIENT_ID'),
        client_secret = os.getenv('CLIENT_SECRET'),
        redirect_uri = os.getenv('REDIRECT_URI'),
    ))

    # Get the playlist ID from environment variables
    playlist_id = os.getenv('YOUR_PLAYLIST_ID')

    new_tracks = convert_to_spotify_track_uris()

    track_ids = []
    offset = 0
    limit = 100

    # Get the total number of tracks in the playlist
    playlist = sp.playlist(playlist_id, fields='tracks.total')
    total_tracks = playlist['tracks']['total']

    while offset < total_tracks:
        # Get the tracks of the playlist with pagination
        results = sp.playlist_tracks(playlist_id, fields='items.track.id', limit=limit, offset=offset)
        tracks = results['items']
        
        # Add track IDs to the list
        for track in tracks:
            track_id = track['track']['id']
            if track_id:
                track_ids.append(track_id)

        offset += limit

    track_ids = ['spotify:track:' + track_id for track_id in track_ids]

    dupes = set(new_tracks).intersection(track_ids)
    dupes = list(dupes)
    chunked_dupes = chunkify(dupes)

    for dupes in chunked_dupes:
        sp.playlist_remove_all_occurrences_of_items(playlist_id, dupes)
       
                 
if __name__ == "__main__":
    playlist_cleaner()