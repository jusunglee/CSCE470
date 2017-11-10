from sklearn.neighbors import BallTree
from feature_generator import FeatureGenerator
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from requests.exceptions import ConnectionError
from spotipy.client import SpotifyException
import numpy
from pprint import pprint

CLIENT_ID = 'c96d60fcd9904999a60b35b17ab7491c'
CLIENT_SECRET = 'ff13291c8d2b43719726d54d1a3a7b25'


def get_training_data(users):
    global spotify_api
    global gen

    done_playlists = set(json.loads(p)[0] for p in open('training.data', 'r'))

    with open('training.data', 'a') as f:
        for user in users:
            for playlist in spotify_api.user_playlists(user)['items']:
                print user, '\t', playlist['name'], '\t', playlist['id']

                if playlist['id'] in done_playlists:
                    continue

                p = spotify_api.user_playlist(user, playlist['id'])
                f.write(json.dumps([p['id'], p['name'], p['uri'], user, gen.process(user, p)]))
                f.write('\n')
                done_playlists.add(p['id'])


def train_classfier():
    global classifier
    global X

    X = [json.loads(d.strip()) for d in open('training.data', 'r')]
    classifier = BallTree([x[4] for x in X])


def test_classifier(user):
    global spotify_api
    global classifier
    global gen
    global X

    for playlist in spotify_api.user_playlists(user)['items']:
        p = spotify_api.user_playlist(user, playlist['id'])
        feature_vec = [p['id'], p['name'], p['uri'], user, gen.process(user, p)]
        dist, ind = classifier.query([feature_vec[4]], k=10)

        print 'Recommend for:', json.dumps(feature_vec)
        for i in range(len(ind[0])):
            if dist[0][i] > 0.005:
                print '\t', dist[0][i], ":", json.dumps(X[ind[0][i]])
        print ''


def test_classifier_song(song):
    global spotify_api
    global classifier
    global gen
    global X

    p = {'tracks': {'items': [
        {}
    ]}}

    feature_vec = [0, None, None, None, gen.process(user, p)]
    dist, ind = classifier.query([feature_vec[4]], k=5)

    print 'Recommend for:', json.dumps(feature_vec)
    for i in range(len(ind[0])):
        print '\t', dist[0][i], ":", json.dumps(X[ind[0][i]])
    print ''


def test_api(user='habeebmh'):
    global spotify_api

    for playlist in spotify_api.user_playlists(user)['items']:
        p = spotify_api.user_playlist(user, playlist['id'])
        feature_vec = gen.process(user, p)
        print feature_vec


if __name__ == '__main__':
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    spotify_api = spotipy.Spotify(
        client_credentials_manager=client_credentials_manager)
    gen = FeatureGenerator(spotify=spotify_api)
    classifier = None
    X = None

    genres = {}
    for line in open('genre_list.txt'):
        kvp = line.strip().split(',')
        genres[kvp[0]] = kvp[1]

    # get_training_data([u.strip() for u in open('users.txt', 'r') if (not u.startswith('#')) and (not u == '')])
    train_classfier()
    test_classifier('habeebmh')
    # test_api()
