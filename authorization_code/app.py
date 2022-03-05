import os
from flask import Flask, redirect, request, session
from flask_session import Session
from spotify_info import export_spotify_info
import spotipy
import uuid

export_spotify_info()

app = Flask(__name__, static_folder=os.getcwd() + '/public')
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


@app.route('/login')
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
        return redirect('/home')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. If not already signed in, redirect to sigin in link
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)

    # Step 4. Signed in
    return redirect('/home')


@app.route('/home')
def home():
    return app.send_static_file('home.html')


@app.route('/sign_out')
def sign_out():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path())
        session.clear()
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    return redirect('/')


@app.route('/current_user')
def current_user():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/room')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user()


if __name__ == '__main__':
    app.run(threaded=True, port=8888)
