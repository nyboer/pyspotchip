#!/usr/bin/env python

"""
Use pyspotify to play a playlist. Use 'n' to go to next track.
Run this file directly without arguments to play a default playlist
    python play_list.py
"""

from __future__ import unicode_literals
from keys import KBHit
import sys
import threading
from track_features import get_analysis
from keys import KBHit
import spotipy #web api for python
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import spotify #libspotify, needed for playback
from creds import spot_username, spot_password #from creds.py

if sys.argv[1:]:
    playlist_index = sys.argv[1]
else:
    playlist_index = 0


# GLOBAL VARIABLES
track_uri = 'spotify:track:7Ke18a4dLDyjdBRNd5iLLM'
    #some other tracks: 5uNlgK7FEg6r9BGy12P9Sx 5GgUWb9o5ga3F7o6MYyDHO 1VsNbze4CN1b1QgVdWlc3K
#let's declare a couple variables that show up around these parts
track_index = 0
track_count = 0
section_count = 0
#for examples of recalling stored playlists
stored_playlists = [1,2]


#track Keyboard presses
kb = KBHit()

# Assuming a spotify_appkey.key in the current dir
session = spotify.Session()

# Connect an audio sink
audio = spotify.AlsaSink(session)

# Process events in the background
loop = spotify.EventLoop(session)
loop.start()
# Events for coordination
logged_in = threading.Event()
end_of_track = threading.Event()

#utility function
def clamp(n, smallest, largest): return max(smallest, min(n, largest))

#callback from libspotify
def on_connection_state_updated(session):
    if session.connection.state is spotify.ConnectionState.LOGGED_IN:
        logged_in.set()

#callback from libspotify
def on_end_of_track(self):
    playlist_track()
def play_pause():
    if player.state == spotify.player.PlayerState.PLAYING:
        session.player.pause()
    elif player.state == spotify.player.PlayerState.PAUSED:
        session.player.play()
    elif player.state == spotify.player.PlayerState.UNLOADED:
        print 'nothing loaded to play'

def playlist_track(tracks):
    global track_index
    global track_uri
    global section_times
    tcount = len(tracks['items'])
    if track_index<tcount:
        current_track = tracks['items'][track_index]['track']
        track_uri = current_track['uri']
        track_name = current_track['name']
        tid = current_track['id']
        track_data = get_analysis([tid]) #this takes several secs
        section_times = track_data.section_times
        print('currently playing: '+track_name+' uri: '+track_uri)
        track = session.get_track(track_uri).load()
        session.player.load(track)
        session.player.play()
        print session.player.state == session.player.PlayerState.PLAYING
        #end_of_track.set()
    #increase track number to play from list. Playback of list is looped by modulo
    track_index = (track_index + 1) % tcount

#add current track to user's saved songs
def add_to_usongs():
    if(token):
        sp_wapi = spotipy.Spotify(token)
        sp_wapi.trace=False
        tid = [ track_uri.split(':')[2] ]
        print ( 'Adding track: '+str(tid) )
        sp_wapi.current_user_saved_tracks_add(tid)
    else:
        print ('no token')

#advance to next track in playlist
def to_next_track():
    print('to next track')
    section_count = 0 #reset for new track.
    session.player.unload()
    playlist_track()

#smart ffd
# if it were really smart, it would log the current playhead time, then move to the next section from "now"
def to_next_section(t):
    if( len(section_times) > 0 ):
        ms = (1000 * section_times[t])-500
        totime = clamp (int( ms ), 0, 3600000) #keep it between 0ms and an hour
        print ('next section at time: '+str(totime))
        session.player.seek(totime)

def start_playlist(i,playlists):
    global track_count, track_index
    track_index = 0 #start at the beginning
    playlist = playlists['items'][i]
    track_count = playlist['tracks']['total']
    print ('playlist name: ' + playlist['name'] + ' & track count %d' % track_count )
    current_playlist = sp.user_playlist(spot_username, playlist['id'],fields="tracks")
    tracks = current_playlist['tracks']
    playlist_track(tracks)

def login():
    #register for Spotify Web API. this is kind of redundant with what happens in track_features.py but...
    client_credentials_manager = SpotifyClientCredentials()
    print('get auth token')
    scope = 'user-library-modify'
    token = util.prompt_for_user_token(spot_username, scope)
    #sp_wapi = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Register event listeners for libspotify
    session.on(spotify.SessionEvent.CONNECTION_STATE_UPDATED, on_connection_state_updated)
    session.on(spotify.SessionEvent.END_OF_TRACK, on_end_of_track)

    # Block until Login for libspotify is complete
    print('\n...Waiting for Login to Complete...')
    session.login(spot_username, spot_password, remember_me=True)
    logged_in.wait()
    print 'logged in as '+session.user_name

    return token

def get_playlists():
    playlists = sp.user_playlists(spot_username)
    pcount = len(playlists['items'])
    print 'User # of playlists: '+str(pcount)
    return playlists

def print_all_tracks(playlists):
    print 'Number of Playlists: '+str( len(playlists['items']) )
    for playlist in playlists['items']:
        print '-  -  -  -'
        print playlist['owner']['id']
        print playlist['name']
        #print playlist['id']
        print ' total tracks', playlist['tracks']['total']
        results = sp.user_playlist(spot_username, playlist['id'], fields="tracks,next")
        tracks = results['tracks']
        show_tracks(tracks)
        while tracks['next']:
            tracks = sp.next(tracks)
            show_tracks(tracks)

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        output = u' '.join( (track['artists'][0]['name'], track['name']) ).encode('utf-8').strip()
        print '  '+str(i)+ ' ' +output

#initialize
token = login()
sp = spotipy.Spotify(auth=token)
playlists = get_playlists()
start_playlist(0,playlists)

# Wait for playback to complete or Ctrl+C or, better, Ctrl+Shift+\. There is probably a better way to do this.

try:
    while not end_of_track.wait(0.1):
        if kb.kbhit():
            c = kb.getch()
            if ord(c) == 27: # ESC
                break
            if ord(c) == 110: # n
                to_next_track()
            if ord(c) == 115: # s
                add_to_usongs()
            if ord(c) == 49: # 1
                start_playlist(stored_playlists[0])
            if ord(c) == 50: # 2
                start_playlist(stored_playlists[1])
            if ord(c) == 46: # .
                to_next_section(section_count)
                section_count = (section_count + 1) % len(section_times)
            if ord(c) == 32: # space
                state = session.player.state
                if state == 'paused':
                    session.player.play()
                    audio.on()
                else:
                    session.player.play(False)
                    audio.off()
        pass
except KeyboardInterrupt:
    pass
