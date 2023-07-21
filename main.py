# See the GPT script from 7/20. I need to ask the following:
# 2. How can I use the Spotify API to get teh URI of a song
    # Really, this can come later. I should get the song to add first.
# 3. What is a redirect URI and what should I use?
    # What should I use if I were running this on Heroku?
# 4. What are scopes and where can I find a list of them?
    # Again, I can ask this later.

# Left off with: I cant get the redirect uri to load

import requests
import os
from dotenv import load_dotenv

def get_access_token():
    # Replace with your Spotify API credentials
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    REDIRECT_URI = "http://localhost/"  # Replace with your redirect URI
    SCOPES = "playlist-modify-public"  # Required scope for modifying a public playlist

    # Check if a refresh token is already available
    try:
        with open("refresh_token.txt", "r") as file:
            refresh_token = file.read().strip()
    except FileNotFoundError:
        refresh_token = None

    if not refresh_token:
        # Generate the authorization URL
        auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPES}"
        print("Please visit the following URL to authorize the application:")
        print(auth_url)

        # Get the authorization code from the user
        auth_code = input("Enter the authorization code from the redirected URL: ")

        # Exchange the authorization code for access and refresh tokens
        token_url = "https://accounts.spotify.com/api/token"
        data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }

        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            refresh_token = token_data["refresh_token"]

            # Save the refresh token for future use
            with open("refresh_token.txt", "w") as file:
                file.write(refresh_token)
        else:
            print("Failed to obtain access and refresh tokens.")
            return None

    else:
        access_token = refresh_access_token(CLIENT_ID, CLIENT_SECRET, refresh_token)

    return access_token

def refresh_access_token(client_id, client_secret, refresh_token):
    # Use the refresh token to get a new access token
    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        return access_token
    else:
        print("Failed to refresh access token.")
        return None

def add_song_to_playlist(access_token, playlist_id, track_uri):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "uris": [track_uri],
    }
    endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code == 201:
        print("Song added to the playlist successfully!")
    else:
        print("Failed to add the song to the playlist.")

def main():
    access_token = get_access_token()
    if access_token:
        playlist_id = os.getenv('YOUR_PLAYLIST_ID')  # Replace with your playlist ID
        track_uri = "spotify:track:4eHbdreAnSOrDDsFfc4Fpm"  # URI for "I Will Always Love You" by Whitney Houston

        add_song_to_playlist(access_token, playlist_id, track_uri)

if __name__ == "__main__":
    main()