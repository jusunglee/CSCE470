from sklearn.neighbors import BallTree
from feature_generator import FeatureGenerator
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from requests.exceptions import ConnectionError
from spotipy.client import SpotifyException
import numpy
import os


CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

class magicalObject:
    def __init__(self):
        print('Initializing...')
        self.client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        self.spotify_api = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
        print('Training...')
        self.gen = FeatureGenerator(spotify=self.spotify_api)
        self.X = [json.loads(d.strip()) for d in open('./training.data', 'r')]
        self.classifier = BallTree([x[4] for x in self.X])
        print('Training complete.')


    def classify_playlist(self, playlist_uri):
        parts = playlist_uri.split(':')
        user = parts[2]
        playlist = parts[4]
        p = self.spotify_api.user_playlist(user, playlist)
        feature_vec = [p['id'], p['name'], p['uri'], user, self.gen.process(p)]
        dist, ind = self.classifier.query([feature_vec[4]], k=5)
        results = []
        for i in range(len(ind[0])):
            results.append(json.dumps(self.X[ind[0][i]]))
        return results


    def classify_song(self, song_uri):
        parts = song_uri.split(':')
        track = self.spotify_api.track(parts[-1])
        p = {'tracks': {'items': [
            {'track': track}
        ]}}
        feature_vec = [track['id'], track['name'], track['uri'], None, self.gen.process(p)]
        dist, ind = self.classifier.query([feature_vec[4]], k=5)
        results = []
        for i in range(len(ind[0])):
            results.append(json.dumps(self.X[ind[0][i]]))
        return results
