# Outstanding questions
# How can I use the Spotify API to get teh URI of a song
# What redirect uri should I use if I were running this on Heroku?
# What are scopes and where can I find a list of them?
    # Again, I can ask this later.
# ! Re-ask the request and tell it that it needs to add multiple songs. I think we need a for loop. May be able to make it myself.

# import libraries
import requests
import os
from tokens import get_access_token
from get_spotify_track_id import get_spotify_track_id


def add_songs_to_playlist(access_token, playlist_id, track_uris):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "uris": [track_uris],
    }
    endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code == 201:
        print("Songs added to the playlist successfully!")
    else:
        print("Failed to add the song to the playlist.")

def main():
    access_token = get_access_token()
    if access_token:
        playlist_id = os.getenv('YOUR_PLAYLIST_ID') 
        spotify_track_ids = get_spotify_track_id()

        add_songs_to_playlist(access_token, playlist_id, spotify_track_ids)

if __name__ == "__main__":
    main()
