from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
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
    results = unicorn.search_for_tracks(string_query)
    return jsonify(results)


@app.route('/playlist/')
@app.route('/playlist/<string_query>')
def search_for_playlist(string_query=None):
    results = unicorn.search_for_playlists(string_query)
    return jsonify(results)


@app.route('/process/playlist/<playlist_uri>')
def process_playlist(playlist_uri=None):
    results = unicorn.classify_playlist(playlist_uri)
    return jsonify(results)


@app.route('/process/track/<track_uri>')
def process_track(track_uri=None):
    results = unicorn.classify_song(track_uri)
    return jsonify(results)


if __name__ == '__main__':
    unicorn = magical_object.magicalObject() # global var
    app.run(use_reloader=True)
