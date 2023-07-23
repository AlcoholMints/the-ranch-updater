# Helper funtion that grabs an access token for main

# import libraries
import requests
import os
from dotenv import load_dotenv


# gets access token
def get_access_token():
    # Define all of the clint IDs
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    REDIRECT_URI = os.getenv('REDIRECT_URI') # may need to replace for heroku. this needs to be updated in spotify as well.
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
