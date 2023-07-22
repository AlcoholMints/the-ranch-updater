# Outstanding questions
# How can I use the Spotify API to get teh URI of a song
# What redirect uri should I use if I were running this on Heroku?
# What are scopes and where can I find a list of them?
    # Again, I can ask this later.
# ! Need to split the list into 100 track chunks and make a presonse for each chunk. See lastest GPT prompt

# import libraries
import requests
import os
from tokens import get_access_token
from get_spotify_track_uris import get_spotify_track_uris

def add_songs_to_playlist(access_token, playlist_id, track_uris):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "uris": track_uris,
    }
    endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    print("Request data:", data)
    response = requests.post(endpoint, headers=headers, json=data)
    print("Response status code:", response.status_code)
    print("Response content:", response.json())
    if response.status_code == 201:
        print("Songs added to the playlist successfully!")
    else:
        print("Failed to add the songs to the playlist.")

def main():
    access_token = get_access_token()
    if access_token:
        playlist_id = os.getenv('YOUR_PLAYLIST_ID') 
        spotify_track_uris = get_spotify_track_uris()
    add_songs_to_playlist(access_token, playlist_id, spotify_track_uris)

if __name__ == "__main__":
    main()