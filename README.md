# Splaylist

### Description

Recommends Spotify playlists using these features:
* Proportion of explicit songs in playlist
* Average playlist energy
* Average playlist liveness 
* Average playlist tempo
* Average playlist speechiness 
* Average playlist acousticness
* Average playlist instrumentalness
* Average playlist danceability
* Average playlist loudness
* Average playlist valence
* Predominant playlist genre

### How to run

##### Requirements

* Spotipy
* Scikit
* Requests
* Numpy

##### From the command line

**You must first properly set the CLIENT\_ID and CLIENT\_SECRET environment variables.** To do so, from the command line, enter
```bash
$ export CLIENT_ID='your_client_id_here'
$ export CLIENT_SECRET='your_client_secret_here'
```
followed by
```bash
$ python test.py
```
where `python` refers to your Python 2 installation.
