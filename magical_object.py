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


    def add_track_info_to_results(self, results):
        for i, arr in enumerate(results):
            username = arr[3]
            playlist_id = arr[0]
            playlist_search = self.spotify_api.user_playlist(username, playlist_id)
            playlist_url = playlist_search['external_urls']['spotify']
            ps = playlist_search['tracks']['items']
            arr.append(playlist_url)
            sub_list = []
            for item in ps:
                track_name = item['track']['name']
                artist_name = item['track']['artists'][0]['name']
                track_url = item['track']['external_urls']['spotify']
                sub_list.append([track_name, artist_name, track_url])
            arr.append(sub_list)
            results[i] = json.dumps(arr)
        # return results
            


    def classify_playlist(self, playlist_uri):
        parts = playlist_uri.split(':')
        user = parts[2]
        playlist = parts[4]
        p = self.spotify_api.user_playlist(user, playlist)
        feature_vec = [p['id'], p['name'], p['uri'], user, self.gen.process(p)]
        dist, ind = self.classifier.query([feature_vec[4]], k=5)
        results = []
        for i in range(len(ind[0])):
            results.append(self.X[ind[0][i]])
        self.add_track_info_to_results(results)
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
            results.append(self.X[ind[0][i]])
        self.add_track_info_to_results(results)
        return results


    def search_for_tracks(self, string_query):
        results = self.spotify_api.search(string_query)['tracks']['items']
        return_list = []
        for result in results:
            return_list.append({
                'song_id': result['id'],
                'song_name': result['name'],
                'artist_name': result['album']['artists'][0]['name'],
                'artist_id': result['album']['artists'][0]['id'],
                'song_uri': result['uri']
            })
        return return_list


    def search_for_playlists(self, string_query):
        results = self.spotify_api.search(string_query, type='playlist')
        return results

