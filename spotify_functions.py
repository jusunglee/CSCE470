import spotipy
import spotipy.util as util
import os
from simplejson import JSONDecodeError


def load_keys():
    """Loads the keys/tokens from keys/keys.txt into a config dict

    This config file is necessary to load/auth api objects, such as spotipy.

    Returns:
        A dict mapping keys to the corresponding token value.

        {'token_1': token_1_val}
    """
    redirect_uri = 'http://localhost/'
    keys = 'keys/spotify_keys.txt'
    config = {'redirect_uri': redirect_uri}

    with open(keys) as file_:
        content = file_.readlines()

    for line in content:
        tokens = line.split('=')
        tokens = [token.strip() for token in tokens]
        config[tokens[0]] = tokens[1]
    return config


def load_spotipy_object(config):
    """Sets up the spotipy.Spotify() object with config.

    Sets up spotipy object with config dict

    Args:
        config: config dict with all the necessary keys/tokens/info

    Returns:
        A configured spotipy.Spotify() object
    """
    scope = 'playlist-modify-public'
    user_token = ''
    sp = None
    username = config['username']
    client_id = config['client_id']
    client_secret = config['client_secret']
    redirect_uri = config['redirect_uri']
    try:
        user_token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    except (AttributeError, JSONDecodeError):
        os.remove(".cache-{username}")
        user_token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    if user_token:
        sp = spotipy.Spotify(auth=user_token)
        sp.trace = False
    return sp





def add_track_to_playlist(username,track_id,playlist_id):
    sp = load_spotipy_object(load_keys())
    mod_track_uri = ['spotify:track:'+track_id]
    return  sp.user_playlist_add_tracks(username, playlist_id, mod_track_uri)
