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
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing user-modify-playback-state',
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


@app.route('/now_playing')
def now_playing():
    return app.send_static_file('now-playing.html')


@app.route('/currently_playing')
def currently_playing():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/now_playing')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    track = spotify.current_user_playing_track()
    if not track is None:
        return track
    return "No track currently playing."


@app.route('/pause_playback')
def pause_playback():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/now_playing')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    spotify.pause_playback()
    return redirect('/now_playing')


@app.route('/start_playback')
def start_playback():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/now_playing')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    spotify.start_playback()
    return redirect('/now_playing')


@app.route('/next_track')
def next_track():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/now_playing')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    spotify.next_track()
    return redirect('/now_playing')


@app.route('/previous_track')
def previous_track():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/now_playing')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    spotify.previous_track()
    return redirect('/now_playing')


@app.route('/search')
def search():
    return app.send_static_file('search.html')


@app.route('/search_track')
def search_track():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/search')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    data = spotify.search(q=request.args.get("q"), limit=10,
                          offset=0, type='track', market=None)
    return data


@app.route('/add_to_queue')
def add_to_queue():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/search')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    spotify.add_to_queue(uri=request.args.get("uri"))
    return redirect('/search')


if __name__ == '__main__':
    app.run(threaded=True, port=8888)
