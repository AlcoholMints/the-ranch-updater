
# ? What redirect uri should I use if I were running this on Heroku?

# import libraries
import requests
import os
from tokens import get_access_token
from get_spotify_track_uris import convert_to_spotify_track_uris, chunkify
from playlist_cleaner import playlist_cleaner


def add_songs_to_playlist(access_token, playlist_id, track_uris):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "uris": track_uris,
    }
    endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code == 201:
        print("Songs added to the playlist successfully!")
    else:
        print("Response status code:", response.status_code)
        print("Response content:", response.json())
        print("Failed to add the songs to the playlist.")

def main():
    access_token = get_access_token()
    playlist_id = os.getenv('YOUR_PLAYLIST_ID') 
    spotify_track_uris = convert_to_spotify_track_uris()
    playlist_cleaner() # deletes duplicates and old songs on exisiting playlist
    if len(spotify_track_uris) > 100:
        spotify_track_uris = chunkify(spotify_track_uris)
        for chunk in spotify_track_uris:
            add_songs_to_playlist(access_token, playlist_id, chunk)
    else:
        add_songs_to_playlist(access_token, playlist_id, spotify_track_uris)

if __name__ == "__main__":
    main()