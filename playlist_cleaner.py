# import libraries
import requests
import os
from tokens import get_access_token
from dotenv import load_dotenv
from get_spotify_track_uris import convert_to_spotify_track_uris

def playlist_cleaner():
    access_token = get_access_token()
    playlist_id = os.getenv('YOUR_PLAYLIST_ID')
    track_uris = convert_to_spotify_track_uris()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Get the current tracks in the playlist
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    response = requests.get(url, headers=headers)
    response_data = response.json()

    # Extract existing track URIs from the response
    existing_track_uris = set()
    if "items" in response_data:
        for item in response_data["items"]:
            if "track" in item and "uri" in item["track"]:
                existing_track_uris.add(item["track"]["uri"])

    # Delete duplicate tracks from the playlist
    for track_uri in existing_track_uris:
        if track_uri in track_uris:
            delete_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
            data = {"tracks": [{"uri": track_uri}]}
            delete_response = requests.delete(delete_url, headers=headers, json=data)
            if delete_response.status_code == 200:
                print(f"Deleted duplicate track: {track_uri}")
            else:
                print("Response status code:", response.status_code)
                print("Response content:", response.json())
                print(f"Failed to delete track: {track_uri}")

# Call the function to add tracks to the playlist
if __name__ == "__main__":
    playlist_cleaner()