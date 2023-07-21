# import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

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