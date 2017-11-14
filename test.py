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


def test_classifier_playlist(playlist_uri):
    global spotify_api
    global classifier
    global gen
    global X

    parts = playlist_uri.split(':')

    user = parts[2]
    playlist = parts[4]

    p = spotify_api.user_playlist(user, playlist)
    feature_vec = [p['id'], p['name'], p['uri'], user, gen.process(p)]
    dist, ind = classifier.query([feature_vec[4]], k=5)

    print 'Recommend for:', json.dumps(feature_vec)
    for i in range(len(ind[0])):
        print '\t', json.dumps(X[ind[0][i]])
    print ''


def test_classifier_song(song_uri):
    global spotify_api
    global classifier
    global gen
    global X

    parts = song_uri.split(':')

    track = spotify_api.track(parts[-1])
    p = {'tracks': {'items': [
        {'track': track}
    ]}}

    feature_vec = [track['id'], track['name'], track['uri'], None, gen.process(p)]
    dist, ind = classifier.query([feature_vec[4]], k=5)

    print 'Recommend for:', json.dumps(feature_vec)
    for i in range(len(ind[0])):
        print '\t', json.dumps(X[ind[0][i]])
    print ''


def train():
    global classifier
    global X

    X = [json.loads(d.strip()) for d in open('./training.data', 'r')]
    classifier = BallTree([x[4] for x in X])


def main():
    global spotify_api
    global gen

    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    spotify_api = spotipy.Spotify(
        client_credentials_manager=client_credentials_manager)
    gen = FeatureGenerator(spotify=spotify_api)


if __name__ == '__main__':
    classifier = None
    X = None
    spotify_api = None
    gen = None

    # Initialization Functions
    main()
    train()

    # Test Functions
    test_classifier_song('spotify:track:03tqyYWC9Um2ZqU0ZN849H')
    test_classifier_playlist('spotify:user:habeebmh:playlist:79RdtV9JQNX99gCDNY6p4v')
