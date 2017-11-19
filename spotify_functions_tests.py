from spotify_functions import *

sp = load_spotipy_object(load_keys())


def run_all_tests():
    test_search()
    test_add_song_to_playlist()


def test_search():
    """Tests the spotipy search function for a song using string query

    Args:
        sp: preconfigured spotipy.Spotify() object

    Returns:
        items: list of json object in the following format:
        {'song_id': '296mmTJOJ904FwHQsSBdDr',
        'song_name': 'Champagne & Sunshine',
        'artist_name': 'PLVTINUM',
        'artist_id': '4V2pR2iSd1g0RZCglrP3jn',
        'song_uri': 'spotify:track:296mmTJOJ904FwHQsSBdDr'}
    """
    items = get_tracks_from_string_query(sp, 'Champagne and Sunshine')
    for item in items:
        print(item, '\n')
    return items


def test_add_song_to_playlist():
    test_song_id = test_search()[0]['song_id']
    playlist_id = ''
    username = ''
    return add_track_to_playlist(username,test_song_id,playlist_id)


run_all_tests()
