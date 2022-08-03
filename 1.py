import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError


os.environ['SPOTIPY_CLIENT_ID'] = "067f8560ceed4bdb8257546f04c5e1c6"
os.environ['SPOTIPY_CLIENT_SECRET'] = "35afac997f144c198afed538fb838204"
os.environ['SPOTIPY_REDIRECT_URI'] = "http://google.com/"

username = "a0ce887b5e994695"
scope = "user-read-private user-read-playback-state user-modify-playback-state"

try:
    token = util.prompt_for_user_token(username, scope)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

spotifyObject = spotipy.Spotify(auth=token)

devices = spotifyObject.devices()
# print(json.dumps(devices,  sort_keys=True, indent=4))
deviceID = devices['devices'][0]['id']

# track = spotifyObject.current_user_playing_track()
# artist = track['item']['artists'][0]['name']
# track = track['item']['name']

# if artist != "":
#     print("Currently Playing " + artist + " - " + track)

user = spotifyObject.current_user()

displayName = user['display_name']
followers = user['followers']['total']

while True:
    print()
    print("Welcome to Spotipy " + displayName + "!" +
          " You have " + str(followers) + " followers.")
    print()
    print("0 - Search for an artist")
    print("1 - exit")
    print()
    choice = input("Your choice: ")
    if choice == "0":
        print()
        searchQuery = input("What is the name of the artist?: ")
        print()
        searchResults = spotifyObject.search(searchQuery, 1, 0, "artist")
        # print(json.dumps(searchResults,  sort_keys=True, indent=4))

        # artist details
        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total'])+" followers")
        print(artist['genres'][0])
        webbrowser.open(artist['images'][0]['url'])
        artistID = artist['id']

        # album and track details
        trackURIs = []
        trackArt = []
        z = 0

        # Extract album details
        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items']

        for item in albumResults:
            print("ALBUM" + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url']

            # track data
            trackResults = spotifyObject.album_tracks(albumID)
            trackResults = trackResults['items']

            for item in trackResults:
                print(str(z) + ": " + item['name'])
                trackURIs.append(item['uri'])
                trackArt.append(albumArt)
                z += 1
            print()

        # See album art
        while True:
            songSelection = input(
                "Enter a song number to see album art and play the song (x to exit): ")  # and play the song
            if songSelection == "x":
                break
            trackSelectionList = []
            trackSelectionList.append(trackURIs[int(songSelection)])
            spotifyObject.start_playback(
                deviceID, None, trackSelectionList)  # added
            webbrowser.open(trackArt[int(songSelection)])

    if choice == "1":
        break

    # print(json.dumps(trackResults, sort_keys=True, indent=4))
