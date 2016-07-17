#!/usr/bin/env python

"""
This is an example of playing music from Spotify using pyspotify.
The example use the :class:`spotify.AlsaSink`, and will thus only work on
systems with an ALSA sound subsystem, which means most Linux systems.
You can either run this file directly without arguments to play a default
track::
    python play_track.py
Or, give the script a Spotify track URI to play::
    python play_track.py spotify:track:3iFjScPoAC21CT5cbAFZ7b
"""

from __future__ import unicode_literals

import sys
import threading
import spotify

from creds import spot_username, spot_password

if sys.argv[1:]:
    track_uri = sys.argv[1]
else:
    track_uri = 'spotify:track:7Ke18a4dLDyjdBRNd5iLLM'
#some other tracks: 5uNlgK7FEg6r9BGy12P9Sx 5GgUWb9o5ga3F7o6MYyDHO 1VsNbze4CN1b1QgVdWlc3K

# Assuming a spotify_appkey.key in the current dir
session = spotify.Session()

# Process events in the background
loop = spotify.EventLoop(session)
loop.start()

# Connect an audio sink
audio = spotify.AlsaSink(session)

# Events for coordination
logged_in = threading.Event()
end_of_track = threading.Event()

def on_connection_state_updated(session):
    if session.connection.state is spotify.ConnectionState.LOGGED_IN:
        print 'connection state updated'
        logged_in.set()

def on_end_of_track(self):
    print 'end of track'
    end_of_track.set()


# Register event listeners
session.on(
    spotify.SessionEvent.CONNECTION_STATE_UPDATED, on_connection_state_updated)
session.on(spotify.SessionEvent.END_OF_TRACK, on_end_of_track)

 # Block until Login is complete
print('Waiting for Login to Complete...')
session.login(spot_username, spot_password, remember_me=True)
print('logging in...')
logged_in.wait()
print('logged in')

# Assuming a previous login with remember_me=True and a proper logout
#session.relogin()
#logged_in.wait()

# Play a track
track = session.get_track(track_uri).load()
session.player.load(track)
session.player.play()


# Wait for playback to complete or Ctrl+C or, better, Ctrl+Shift+\. There is probably a better way to do this.
try:
    while not end_of_track.wait(0.1):
        pass
except KeyboardInterrupt:
    pass
