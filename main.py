import spotipy
import time
import sys
import json
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
import csv


# long_term (calculated from several years of data and including all new data as it becomes available), medium_term (approximately last 6 months), short_term (approximately last 4 weeks
# The key the track is in. Integers map to pitches using standard Pitch Class notation. E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1. [-1,11]
# The popularity of a track is a value between 0 and 100, with 100 being the most popular.The popularity is calculated by algorithm and is based, in the most part,
# on the total number of plays the track has had and how recent those plays are.

def GetTracks(playlist: str) -> list:
    spotifyObject = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    offset = 0
    playlist_songs = []
    while True:
        response = spotifyObject.playlist_items(playlist_id=playlist,
                                                offset=offset,
                                                fields='items.track.id,total',
                                                additional_types=['track'])

        if len(response['items']) == 0:
            print('all songs appended to list')
            break
        for i in response['items']:
            playlist_songs.append(i['track']['id'])
        offset = offset + len(response['items'])
        print('offset is: ', offset)
    return playlist_songs


def GetFeatures(songIDs: list) -> dict:
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    sp.trace = True
    songFeatures = []
    count = 0
    for i in songIDs:
        count += 1
        if count % 10 == 0:
            print('Song number', count, 'added')
        artists = []
        artistlinks = []
        track = sp.track(i)
        for artist in track['artists']:  # make a list of artists names and convert them into one string separated by a comma
            artistlinks.append(artist['external_urls']['spotify'])
            artists.append(artist['name'])
        artists = ' | '.join([str(x) for x in artists])
        artistlinks = ' | '.join([str(x) for x in artistlinks])
        features = sp.audio_features(i)
        tempdict = {'name': track['name']}
        tempdict.update({'artist': artists})
        tempdict.update({'artist_links' : artistlinks})
        tempdict.update({'release_date': track['album']['release_date']})
        tempdict.update({'popularity': track['popularity']})
        tempdict.update(features[0])  # eg acousticness, danceability
        songFeatures.append(tempdict)
    return songFeatures


def ExportToCSV(features: dict):
    column_names = ['acousticness', 'analysis_url', 'artist', 'artist_links', 'danceability', 'duration_ms', 'energy', 'id',
                    'instrumentalness',
                    'key', 'liveness', 'loudness', 'mode', 'name', 'release_date', 'popularity', 'speechiness', 'tempo',
                    'time_signature',
                    'track_href',
                    'type', 'uri', 'valence']
    if len(features) > 1:
        csv_name = 'sussy.csv'
        print('updated sussy')
    else:
        print('updated userTrack')
        csv_name = 'userTrack.csv'
    with open(csv_name, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, column_names)
        w.writeheader()
        w.writerows(features)
        f.close()


if __name__ == '__main__':
    #Tracks = GetTracks('https://open.spotify.com/playlist/22NJNtoxRmGdDWfSrQ9ve6?si=f8d653200c1b4843')
    #features = GetFeatures(Tracks)
    print('got playlist tracks')
    #ExportToCSV(features)
    currentUserTrack = GetFeatures(['5sysgWS6HwrfhHDnqMh27l'])
    print('got features')
    ExportToCSV(currentUserTrack)

