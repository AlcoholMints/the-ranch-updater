# import libraries
import requests
import os
from tokens import get_access_token
from dotenv import load_dotenv
from get_spotify_track_uris import convert_to_spotify_track_uris
from datetime import datetime, timedelta

def playlist_cleaner():

    # * Initializing data
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

    # * Remove the duplicates from the playlist loops
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
                continue
            else:
                print("Response status code:", response.status_code)
                print("Response content:", response.json())
                print(f"Failed to delete track: {track_uri}")

    # * Remove the old songs loops
    # Extract existing track URIs and their added dates from the response
    existing_tracks = {}
    if "items" in response_data:
        for item in response_data["items"]:
            if "track" in item and "uri" in item["track"] and "added_at" in item:
                track_uri = item["track"]["uri"]
                added_at = item["added_at"]
                existing_tracks[track_uri] = added_at

    # Remove songs added over 30 days ago
    thirty_days_ago = datetime.now() - timedelta(days=30)
    thirty_days_ago_timestamp = thirty_days_ago.timestamp()
    for track_uri, added_at in existing_tracks.items():
        # Parse the added_at date to a datetime object
        added_date = datetime.strptime(added_at, "%Y-%m-%dT%H:%M:%S%z")
        # Convert added_date to a numeric timestamp value
        added_date_timestamp = added_date.timestamp()
        # Compare the added date with the date 30 days ago
        if added_date_timestamp < thirty_days_ago_timestamp:
            delete_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
            data = {"tracks": [{"uri": track_uri}]}
            delete_response = requests.delete(delete_url, headers=headers, json=data)
            if delete_response.status_code == 200:
                continue
            else:
                print(f"Failed to delete old track: {track_uri} (added on {added_date})")


if __name__ == "__main__":
    playlist_cleaner()