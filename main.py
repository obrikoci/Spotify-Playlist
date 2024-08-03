from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# --------------------------------------------------INFROMATION--------------------------------------------------------
# from spotipy
CLIENT_ID = "client id"
CLIENT_SECRET = "client secret"
REDIRECT_URI = "http://example.com"
USERNAME = "username"
SCOPE = "playlist-modify-public"
access_token = "token"
# ------------------------------------------------GETTING HOLD OF SONGS------------------------------------------------
user_date = input("What year would you want to travel to? "
                  "Type in the answer in this format YYYY-MM-DD):")

year = user_date.split("-")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{user_date}/")
date_website = response.text

soup = BeautifulSoup(date_website, "html.parser")
songs_tags = soup.find_all(name="h3", id="title-of-a-story")
songs = []
for song in songs_tags:
    title = song.getText().strip()
    songs.append(title)
title_songs = songs[6:-13:4]

song_artists = soup.select(selector="li span")
names = []
for artist in song_artists:
    name = artist.getText().strip()
    names.append(name)
new_names = names[16:-38]

while "NEW" in new_names:
    new_names.remove("NEW")
while "RE-\nENTRY" in new_names:
    new_names.remove("RE-\nENTRY")
artists = new_names[::8]

all_songs = []
for n in range(0, 100):
    print(f"{title_songs[n]} by {artists[n]}")
# ------------------------------------------------CREATING PLAYLIST----------------------------------------------------
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE,
                                               username=USERNAME))
my_playlist = f"{user_date} Top Songs"
playlist_description = f"The top 100 songs played on the week of {user_date}"
playlist = sp.user_playlist_create(user=USERNAME, name=my_playlist, description=playlist_description)
print(f"Playlist '{my_playlist}' created successfully with ID: {playlist['id']}")
# ------------------------------------------------ADDING TRACKS--------------------------------------------------------
track_uris = []
for n in range(0, 100):
    search_query = f"track:{title_songs[n]} artist:{artists[n]}"
    results = sp.search(q=search_query, limit=1)

    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        track_uris.append(track_uri)
    else:
        track_uri = None

if track_uris:
    sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris)
    print(f"Tracks added to playlist '{my_playlist}'")
else:
    print("No tracks to add to the playlist.")
