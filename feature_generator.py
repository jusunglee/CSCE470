from __future__ import division
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
import json
import numpy
import collections
# % explicit, avg popularity, avg energy, avg liveness, avg tempo, avg speechiness, avg acousticness,


class FeatureGenerator():

    def __init__(self, spotify=None, client_id=None, client_secret=None):
        if spotify:
            self.spotify_api = spotify
        elif client_id and client_secret:
            client_credentials_manager = SpotifyClientCredentials(
                client_id=client_id, client_secret=client_secret)
            self.spotify_api = spotipy.Spotify(
                client_credentials_manager=client_credentials_manager)
        else:
            raise ValueError(
                'A Spotipy API instance or Credentials must be specified.')

        self.genres = {}
        for line in open('genre_list.txt'):
            kvp = line.strip().split(',')
            self.genres[kvp[1]] = kvp[0]

    def track_genre(self, t):
        artist_ids = [a['id'] for a in t['artists']]
        genres = []
        for uid in artist_ids:
            genres.extend(self.spotify_api.artist(uid)['genres'])
        return genres


    def track_features(self, t):
        audio_features = self.spotify_api.audio_features(
            'spotify:track:{}'.format(t['id']))[0]

        r = [
            1 if t['explicit'] == True else 0,
            # t['popularity'],
            audio_features['energy'],
            audio_features['liveness'],
            audio_features['tempo'],
            audio_features['speechiness'],
            audio_features['acousticness'],
            audio_features['instrumentalness'],
            # audio_features['time_signature'],
            audio_features['danceability'],
            # audio_features['duration_ms'],
            audio_features['loudness'],
            audio_features['valence']
        ]
        # print t['name'], r
        return [numpy.nan if x is None else x for x in r]

    def process(self, user, playlist):
        results = []

        p = self.spotify_api.user_playlist(user, playlist)
        track_features = [self.track_features(track['track'])
                  for track in p['tracks']['items']]

        genres = {}
        for track in p['tracks']['items']:
            for g in self.track_genre(track['track']):
                if g in genres:
                    genres[g] += 1
                else:
                    genres[g] = 1

        track_feature = numpy.nanmean(track_features, axis=0)
        genre = max(genres.iteritems(), key=lambda x: x[1])[0]

        results.extend(track_feature)
        results.append(self.genres[genre])

        return results
