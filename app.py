import os
from flask import Flask, redirect, request, session, render_template
from urllib.parse import urlencode
import spotipy
import uuid

app = Flask(__name__, instance_path='/instance')
app.secret_key = os.urandom(64)

caches_folder = './instance/.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)


def session_cache_path():
    return caches_folder + session.get('roomid')


def roomid_cache_path(roomid):
    return caches_folder + roomid


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    if not session.get('roomid'):
        # Step 1. give random ID
        session['roomid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing user-modify-playback-state',
                                               cache_handler=cache_handler,
                                               show_dialog=True)

    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/home' + '?' + urlencode({'roomid': session.get('roomid')}))

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. If not already signed in, redirect to sigin in link
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)

    # Step 4. Signed in
    return redirect('/home' + '?' + urlencode({'roomid': session.get('roomid')}))


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/sign_out')
def sign_out():
    try:
        # Remove the CACHE file
        os.remove(roomid_cache_path(request.args.get("roomid")))
        session.clear()
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    return redirect('/')


@ app.route('/current_user')
def current_user():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=roomid_cache_path(request.args.get("roomid")))
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/room')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user()


@ app.route('/now_playing')
def now_playing():
    return render_template('now-playing.html')


@ app.route('/currently_playing')
def currently_playing():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=roomid_cache_path(request.args.get("roomid")))
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/now_playing')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    track = spotify.current_user_playing_track()
    if not track is None:
        return track
    return "No track currently playing."


@ app.route('/pause_playback')
def pause_playback():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=roomid_cache_path(request.args.get("roomid")))
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/now_playing')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    spotify.pause_playback()
    return redirect('/now_playing')


@ app.route('/start_playback')
def start_playback():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=roomid_cache_path(request.args.get("roomid")))
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/now_playing')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    spotify.start_playback()
    return redirect('/now_playing')


@ app.route('/next_track')
def next_track():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=roomid_cache_path(request.args.get("roomid")))
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/now_playing')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    spotify.next_track()
    return redirect('/now_playing')


@ app.route('/previous_track')
def previous_track():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=roomid_cache_path(request.args.get("roomid")))
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/now_playing')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    spotify.previous_track()
    return redirect('/now_playing')


@ app.route('/search')
def search():
    return render_template('search.html')


@ app.route('/search_track')
def search_track():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=roomid_cache_path(request.args.get("roomid")))
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/search')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    data = spotify.search(q=request.args.get("q"), limit=10,
                          offset=0, type='track', market=None)
    return data


@ app.route('/add_to_queue')
def add_to_queue():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=roomid_cache_path(request.args.get("roomid")))
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/search')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    spotify.add_to_queue(uri=request.args.get("uri"))
    return redirect('/search')


if __name__ == '__main__':
    app.run(threaded=True,
            port=int(os.environ.get('PORT', 8888)))
