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
        for line in open('./func_files/genre_list.txt'):
            kvp = line.strip().split(',')
            self.genres[kvp[1]] = kvp[0]

    def track_genre(self, t):
        artist_ids = [a['id'] for a in t['artists']]
        genres = []
        for uid in artist_ids:
            try:
                genres.extend(self.spotify_api.artist(uid)['genres'])
            except:
                continue
        return genres

    def track_features(self, t):
        audio_features = None
        try:
            audio_features = self.spotify_api.audio_features(
                'spotify:track:{}'.format(t['id']))[0]
        except:
            audio_features = {
                'energy': numpy.nan,
                'liveness': numpy.nan,
                'tempo': numpy.nan,
                'speechiness': numpy.nan,
                'acousticness': numpy.nan,
                'instrumentalness': numpy.nan,
                'danceability': numpy.nan,
                'loudness': numpy.nan,
                'valence': numpy.nan
            }

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

        return [numpy.nan if x is None else x for x in r]

    def process(self, p):
        results = []

        track_features = [n for n in [self.track_features(track['track']) for track in p[
            'tracks']['items']] if n is not None]

        genres = {}
        for track in p['tracks']['items']:
            for g in self.track_genre(track['track']):
                if g in genres:
                    genres[g] += 1
                else:
                    genres[g] = 1

        track_feature = numpy.nanmean(track_features, axis=0)

        genre = None
        while len(genres):
            test_genre = max(genres.iteritems(), key=lambda x : x[1])
            if test_genre[0] in self.genres:
                genre = test_genre[0]
                break
            genres.pop(test_genre[0])
        #print genre

        results.extend(track_feature)
        results.append(float(self.genres[genre]))

        return results
