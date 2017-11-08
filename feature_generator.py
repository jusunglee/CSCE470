from __future__ import division
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
import json
import numpy

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
        tracks = [self.track_features(track['track'])
                  for track in p['tracks']['items']]
        

        track_features = numpy.nanmean(tracks, axis=0)

        results.extend(track_features)

        return results
