import os
from urllib import response
from flask import Flask, make_response, redirect, request, session
from flask_session import Session
from spotify_info import export_spotify_info
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import urllib.parse
import requests
import uuid

export_spotify_info()

app = Flask(__name__, static_folder='./public')
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)


def session_cache_path():
    return caches_folder + session.get('uuid')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@ app.route('/login')
def login():
    if not session.get('uuid'):
        # Step 1. Visitor is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing playlist-modify-private',
                                               cache_handler=cache_handler,
                                               show_dialog=True)

    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        token_info = auth_manager.get_access_token(request.args.get("code"))
        return redirect('/#' +
                        urllib.parse.urlencode({
                            'access_token': token_info['access_token'],
                            'refresh_token': token_info['refresh_token']})
                        )

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. If not already signed in, redirect to sigin in link
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)

    # Step 4. Signed in
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    token_info = cache_handler.get_cached_token()
    return redirect('/#' +
                    urllib.parse.urlencode({
                        'access_token': token_info['access_token'],
                        'refresh_token': token_info['refresh_token']})
                    )


@app.route('/sign_out')
def sign_out():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path())
        session.clear()
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    return redirect('/')


if __name__ == '__main__':
    app.run(threaded=True, port=8888)