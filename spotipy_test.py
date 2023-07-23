# import libraries
# ! right now, this is addingto playlist, i want it to just edit the list and then put it back into main
import requests
import os
from tokens import get_access_token
from dotenv import load_dotenv
from get_spotify_track_uris import get_spotify_track_uris

def add_tracks_to_playlist():
    access_token = get_access_token()
    playlist_id = os.getenv('YOUR_PLAYLIST_ID')
    track_uris = get_spotify_track_uris()

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

    # Remove any duplicates from the list of track URIs
    track_uris_without_duplicates = []
    for track_uri in track_uris:
        if track_uri not in existing_track_uris:
            track_uris_without_duplicates.append(track_uri)

    # Delete duplicate tracks from the playlist
    for track_uri in existing_track_uris:
        if track_uri not in track_uris:
            delete_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
            data = {"tracks": [{"uri": track_uri}]}
            delete_response = requests.delete(delete_url, headers=headers, json=data)
            if delete_response.status_code == 200:
                print(f"Deleted track: {track_uri}")
            else:
                print(f"Failed to delete track: {track_uri}")

    # Add new tracks to the playlist, avoiding duplicates
    if track_uris_without_duplicates:
        add_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        data = {"uris": track_uris_without_duplicates}
        add_response = requests.post(add_url, headers=headers, json=data)

        if add_response.status_code == 201:
            print("Tracks added successfully!")
        else:
            print("Failed to add tracks to the playlist.")
            print(f"Response: {add_response.json()}")

# Call the function to add tracks to the playlist
if __name__ == "__main__":
    add_tracks_to_playlist()