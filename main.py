from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from pprint import pprint

# setup song webpage to scrape
# date = input('input date yyyy-mm-dd: ')
date = '1996-07-20'  # input date to find top 100 songs for
url = 'https://www.billboard.com/charts/hot-100/' + date
# print(url)
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")  # get html data for top 100 songs
# print(soup)
# print(soup.prettify())

#get song names
song_data = soup.find_all("h3", id="title-of-a-story", class_='u-line-height-125')
artist_data = soup.find_all("span", class_='u-max-width-330')
song_names = []
artist_names = []
for song in song_data:
    song = song.getText().strip()
    song = song.split('/')[0]
    song_names.append(song)
for artist in artist_data:
    artist = artist.getText().strip()
    artist = artist.split('Featuring')[0]
    artist_names.append(artist)

# song_names = [name.getText().strip() for name in song_data]
# artist_names = [name.getText().strip() for name in artist_data]

# print(song_names)
# print(len(song_names))
# print(artist_names)
# print(len(artist_names))

# create connection with spotify api
SPOTIPY_CLIENT_ID = 'SPOTIPY_CLIENT_ID'
SPOTIPY_CLIENT_SECRET = 'SPOTIPY_CLIENT_SECRET'
SPOTIPY_REDIRECT_URI = 'http://example.com'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=SPOTIPY_REDIRECT_URI,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user = sp.current_user()
user_id = user['id']
print(user_id)

# q = f'track:{song_names[2]} artist:{artist_names[2]}'
# # q = f'track:{song_names[0]} year:1996'
# print(q)
# song = sp.search(q, type="track")
# pprint(song)
# print(song['tracks']['total'])
# print(song['tracks']['items'][0]['uri'])

# try and find songs on spotify
song_uris = []
for idx, track in enumerate(song_names):
    # q = f'track:{song_names[idx]} artist:{artist_names[idx]}'
    q = f'track:{song_names[idx]}'
    song = sp.search(q, type="track")
    try:
        uri = song['tracks']['items'][0]['uri']
        song_uris.append(uri)
    except IndexError:
        print(f'Number {idx}: {track} not found')
    time.sleep(0.01)

# print(song_uris)
# print(len(song_uris))

# make playlist:
playlist_name = date + ' Billboard 100'

# create playlist
playlist = sp.user_playlist_create(user_id, playlist_name, False)
# print(playlist)

# add songs to playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
# print(playlist)

# playlist_url = 'https://api.spotify.com/v1/users/'+user_id+'/playlists'
# params = {
#     "name": "playlist_name",
#     "description": "Test auto playlist",
#     "public": False
# }

# playlist_response = requests.post(
#         url=playlist_url,
#         params=params
#     )

# print(playlist_response)