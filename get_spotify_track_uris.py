# datagrabber function
# * Function that grabs all the song and artists played on 95.9 that day in a list
# import libraries
import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

# goes to online radio box and gets the artists and tracks from 95.9
def data_grabber():
    song_list = []
    for day in range(1,7):
        # Create a URL object
        url = f'https://onlineradiobox.com/us/kfwr/playlist/{day}?cs=us.kfwr'

        # Create object page
        page = requests.get(url)

        # parser-lxml - Change html to a Python friendly format
        # obtain the page's information
        soup = BeautifulSoup(page.text, 'html5lib')
        # grab the table on the front, the songs played that day
        song_table = soup.find('table')
        # pull all "a" from the table and put into another list of songs
        for i in song_table.find_all('a'):
            title = i.text
            song_list.append(title)
    return song_list

# Goes to spotify and gets the track uris
def convert_to_spotify_track_uris():
    # Get the song list
    song_list = data_grabber()

    # Initialize Spotipy with nevessary scopes and authentication
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope = "playlist-modify-public",
        client_id = os.getenv('CLIENT_ID'),
        client_secret = os.getenv('CLIENT_SECRET'),
        redirect_uri = os.getenv('REDIRECT_URI'),
    ))

    track_uris = []
    for song_artist in song_list:
        # Split the song_artist string into artist and song parts
        artist_song = song_artist.split(' - ')

        # Check if the artist and song are provided in the correct format
        if len(artist_song) != 2:
            print(f"Invalid format for song_artist: {song_artist}")
            continue

        artist, song = artist_song
        query = f'{artist} {song}'

        # Make the API request to search for the track
        results = sp.search(q=query, type="track", limit=1)

        # Check if the request was successful
        if results["tracks"]["items"]:
            track_uris.append(results["tracks"]["items"][0]["uri"])
        else:
            print(f"Track not found for: {query}")

    spotify_track_uris = remove_internal_duplicates(track_uris)
    return spotify_track_uris

# function that makes the list into a new list comprised of several sublists of size 100 or less
def chunkify(list):
    return [list[i:i + 100] for i in range(0, len(list), 100)]

# for removing duplicates from 95.9 data. used in next function
def remove_internal_duplicates(list):
    # Use a dict to keep track of unique items while preserving order
    seen = {}
    return [seen.setdefault(x, x) for x in list if x not in seen]

if __name__ == "__main__":
    convert_to_spotify_track_uris()