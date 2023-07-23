# datagrabber function
# * Function that grabs all the song and artists played on 95.9 that day in a list
# ? Then it converts to a list of spotify track ids?

# import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tokens import get_access_token

# goes to online radio box and gets the artists and tracks from 95.9
def data_grabber():
    # Create a URL object
    url = 'https://onlineradiobox.com/us/kfwr/playlist/1?cs=us.kfwr'

    # Create object page
    page = requests.get(url)

    # parser-lxml - Change html to a Python friendly format
    # obtain the page's information
    soup = BeautifulSoup(page.text, 'lxml')
    # grab the table on the front, the songs played that day
    song_table = soup.find('table')
    # pull all "a" from the table and put into another list of songs
    song_list = []
    for i in song_table.find_all('a'):
        title = i.text
        song_list.append(title)
    return song_list

# for removing duplicates from 95.9 data. used in next function
def remove_internal_duplicates(list):
    # Use a dict to keep track of unique items while preserving order
    seen = {}
    return [seen.setdefault(x, x) for x in list if x not in seen]


# Goes to spotify and gets the track uris
def convert_to_spotify_track_uris():
    # Get the song list and the access token
    song_list = data_grabber()
    access_token = get_access_token()

    base_url = 'https://api.spotify.com/v1/search'
    headers = {'Authorization': f'Bearer {access_token}'}

    track_ids = []
    spotify_track_uris = []
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
        params = {
            'q': query,
            'type': 'track',
            'limit': 1
        }
        response = requests.get(base_url, headers=headers, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            tracks = data.get('tracks', {}).get('items', [])
            if tracks:
                track_ids.append(tracks[0]['id'])
            else:
                print(f"Track not found for: {query}")
        else:
            print("Response status code:", response.status_code)
            print("Response content:", response.json())
            print(f"Error fetching data for: {query}")

    spotify_track_uris_with_duplicates = ['spotify:track:' + track_id for track_id in track_ids]

    spotify_track_uris = remove_internal_duplicates(spotify_track_uris_with_duplicates)
    return spotify_track_uris

# function that makes the list into a new list comprised of several sublists of size 100 or less
def chunkify(list):
    return [list[i:i + 100] for i in range(0, len(list), 100)]

if __name__ == '__main__':
    convert_to_spotify_track_uris()