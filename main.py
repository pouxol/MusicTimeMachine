from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import *
import pprint

pp = pprint.PrettyPrinter(indent=4)

date = input("What date do you want to travel to (YYYY-MM-DD)?: ")

base_url = "https://www.billboard.com/charts/hot-100/"

response = requests.get(f"{base_url}{date}").text

soup = BeautifulSoup(response, "html.parser")

ranks = soup.find_all(name="span", class_="chart-element__rank__number")
songs = soup.find_all(name="span", class_="chart-element__information__song")
artists = soup.find_all(name="span", class_="chart-element__information__artist")

ranks = [rank.getText() for rank in ranks]
songs = [song.getText() for song in songs]
artists = [artist.getText() for artist in artists]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientID,
                                               client_secret=clientSecret,
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private"))

user_id = sp.current_user()["id"]

uris = []

for i in range(len(ranks)):
    query = f"artist: {artists[i]} track: {songs[i]}"
    s_result = sp.search(q=query)
    # pp.pprint(s_result["tracks"]["items"][0]["uri"])
    try:
        uris.append(s_result["tracks"]["items"][0]["uri"])
    except IndexError:
        pass


playlist_id = sp.user_playlist_create(user_id, f"Music of {date}", public=False)

sp.playlist_add_items(playlist_id["id"], uris)
