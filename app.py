from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import spotify_functions as sf
import magical_object
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/searchtracks')
def searchtracks():
    return render_template('searchtracks.html')


@app.route('/searchplaylists')
def searchplaylists():
    return render_template('searchplaylists.html')


# function that searches for songs based on a keyword.
@app.route('/track/')
@app.route('/track/<string_query>')
def get_search_track(string_query=None):
    sp = sf.load_spotipy_object(sf.load_keys())
    return jsonify(sf.get_tracks_from_string_query(sp, string_query))


@app.route('/playlist/')
@app.route('/playlist/<string_query>')
def search_for_playlist(string_query=None):
    sp = sf.load_spotipy_object(sf.load_keys())
    results = sf.search_for_playlists(sp, string_query)
    print(results)
    return jsonify(results)


@app.route('/process/playlist/<playlist_uri>')
def process_playlist(playlist_uri=None):
    results = unicorn.classify_playlist(playlist_uri)
    return jsonify(results)


@app.route('/process/track/<track_uri>')
def process_track(track_uri=None):
    results = unicorn.classify_song(track_uri)
    return jsonify(results)


app.run(use_reloader=True)
unicorn = magical_object.magicalObject() # global var
    
    