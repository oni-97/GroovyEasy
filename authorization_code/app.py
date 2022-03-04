from os import access
from urllib import response
from flask import Flask, make_response, redirect, request
import clientInfo
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import urllib.parse
import math
import random
import base64
import requests
import json

STATE_KEY = 'spotify_auth_state'
app = Flask(__name__, static_folder='./public')

CONNECT_TIMEOUT = 10.0
READ_TIMEOUT = 30.0

client_id = clientInfo.getClientId()
client_secret = clientInfo.getClientSecret()
redirect_uri = clientInfo.getRedirectUri()


@app.route('/')
def index():
    return app.send_static_file('index.html')


def generate_random_string(length):
    text = ''
    possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    for num in range(length):
        text += possible[math.floor(random.random()*len(possible))]
    return text


@ app.route('/login')
def login():
    # your application requests authorization
    state = generate_random_string(16)
    scope = 'user-read-private user-read-email'
    response = make_response(
        redirect(
            'https://accounts.spotify.com/authorize?' +
            urllib.parse.urlencode({
                'response_type': 'code',
                'client_id': client_id,
                'scope': scope,
                'redirect_uri': redirect_uri,
                'state': state
            })
        )
    )
    response.set_cookie(STATE_KEY, state)
    return response


@ app.route('/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    stored_state = request.cookies.get(STATE_KEY)

    if (state is None) or (state != stored_state):
        return redirect(
            '/#' +
            urllib.parse.urlencode({
                'eroor': 'state_mismatch'
            })
        )

    else:
        try:
            data = {
                'code': code,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code'
            }
            headers = {
                'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode('utf-8')).decode('utf-8')
            }
            post_response = requests.post(
                'https://accounts.spotify.com/api/token',
                headers=headers,
                data=data,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
            )
        except requests.exceptions.Timeout:
            response = make_response(
                redirect(
                    '/#' +
                    urllib.parse.urlencode({
                        'eroor': 'time_out'
                    })
                )
            )
            response.delete_cookie(STATE_KEY)
            return response

        if post_response.status_code == 200:
            json_data = post_response.json()
            access_token = json_data['access_token']
            refresh_token = json_data['refresh_token']

            response = make_response(
                redirect(
                    '/#' +
                    urllib.parse.urlencode({
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    })
                )
            )
            response.delete_cookie(STATE_KEY)
            return response
        else:
            response = make_response(
                redirect(
                    '/#' +
                    urllib.parse.urlencode({
                        'eroor': 'invalid_token'
                    })
                )
            )
            response.delete_cookie(STATE_KEY)
            return response


@ app.route('/refresh_token')
def get_refreshed_access_token():
    refresh_token = request.args.get('refresh_token')
    try:
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        headers = {
            'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode('utf-8')).decode('utf-8')
        }
        post_response = requests.post(
            'https://accounts.spotify.com/api/token',
            headers=headers,
            data=data,
            timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
        )
    except requests.exceptions.Timeout:
        return

    if post_response.status_code == 200:
        json_data = post_response.json()
        access_token = json_data['access_token']

        response = make_response({'access_token': access_token})
        return response


app.run(port=8888, debug=True)