# datagrabber function
# * Function that grabs all the song and artists played on 95.9 that day in a list
# ? Then it converts to a list of spotify track ids?

# import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tokens import get_access_token

def data_grabber():
    # Create a URL object
    url = 'https://onlineradiobox.com/us/kfwr/playlist/?cs=us.kfwr'

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

def get_spotify_track_uris():
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
            print(f"Error fetching data for: {query}")

    spotify_track_uris = ['spotify:track:' + track_id for track_id in track_ids]
    return spotify_track_uris

if __name__ == '__main__':
    get_spotify_track_uris()