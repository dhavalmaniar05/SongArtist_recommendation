import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

# setting up the environment variables
os.environ['SPOTIPY_CLIENT_ID'] = "067f8560ceed4bdb8257546f04c5e1c6"
os.environ['SPOTIPY_CLIENT_SECRET'] = "35afac997f144c198afed538fb838204"
os.environ['SPOTIPY_REDIRECT_URI'] = "http://google.com/"

username = "a0ce887b5e994695"
# this helps in the playback of the songs
scope = "user-read-private user-read-playback-state user-modify-playback-state user-follow-read"

# authenticating the useranme
try:
    token = util.prompt_for_user_token(username, scope)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

# making the spotify object
spotifyObject = spotipy.Spotify(auth=token)

# print(json.dumps(VARIABLE,  sort_keys=True, indent=4)) this can be used to print the json data in a way where it is readable

# user data
user = spotifyObject.current_user()

displayName = user['display_name']
followers = user['followers']['total']

print("Hi " + displayName + " welcome to spotipy! You have " +
      str(followers) + " follower(s)")


albumName = input("Which album do you want to search for: ")
searchResults = spotifyObject.search(albumName, 1, 0, "album")
albumId = searchResults['albums']['items'][0]['id']
albumTracks = spotifyObject.album_tracks(albumId)
albumTracks = albumTracks['items']
# print(json.dumps(albumTracks,  sort_keys=True, indent=4))
trackURIs = []
for items in albumTracks:
    trackURIs.append(items['uri'])
for i in trackURIs:
    print(i)
    print()
#tracks = albumTracks['items'][0]['id']
# trackDetails = spotifyObject.track(tracks[0])
# trackPopularity = trackDetails['popularity']
# print(trackPopularity)
# print(json.dumps(trackDetails,  sort_keys=True, indent=4))
# userTopartists = spotifyObject.current_user_top_artists(
#     2, offset=0, time_range="short")
# print(json.dumps(userTopartists,  sort_keys=True, indent=4))

# userTopartists = userTopartists['artists']['items']
# z = 0

# print("Your top artists are: ")

# for item in userTopartists:
#     print()
#     print(str(z) + item['name'])
#     z += 1

# userToptracks = spotifyObject.current_user_top_tracks
