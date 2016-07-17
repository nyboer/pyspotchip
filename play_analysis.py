#!/usr/bin/env python

"""
This uses the spotify web API to get analysis data for the track.
The analysis is used to create a "smart fast forward" that advances
to sections of the song (n-key).
It also uses the analysis data to send note data over OSC to a synthesizer
creating a very strange sort of automatic accompianment.

Need to call by settings credentials in environment variables.
Here's a shell script that can do that:
----------------
#!/bin/bash

#call this pseudoscript like:
# $ . spotcreds.bash
# or
# $ source spotcreds.bash

export SPOTIPY_CLIENT_ID='f6b5e0293b1446fbbd9402c1f365085e'
export SPOTIPY_CLIENT_SECRET='ec56c12525ce49fbb19f442e0916a52b'
export SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'
export LD_LIBRARY_PATH=/usr/local/lib

python play_analysis.py
----------------


"""

from __future__ import unicode_literals

import sys
from keys import KBHit
import threading
import time
import spotify
from track_features import get_analysis
from osc_tx import oscsend
from creds import spot_username, spot_password

if sys.argv[1:]:
    track_uri = sys.argv[1]
else:
    track_uri = 'spotify:track:1ZPlNanZsJSPK5h9YZZFbZ'
#some other tracks: 7Ke18a4dLDyjdBRNd5iLLM 5uNlgK7FEg6r9BGy12P9Sx 5GgUWb9o5ga3F7o6MYyDHO 1VsNbze4CN1b1QgVdWlc3K 11hqMWwX7sF3sOGdtijofF

#track Keyboard presses
kb = KBHit()

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

section_times = list()
timecount = 0

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

def on_connection_state_updated(session):
    if session.connection.state is spotify.ConnectionState.LOGGED_IN:
        logged_in.set()

def on_end_of_track(self):
    end_of_track.set()

def to_next(t):
    global starttime
    ms = (1000 * section_times[t])-500
    totime = clamp (int( ms ), 0, 3600000) #keep it between 0ms and an hour
    starttime = time.time() - (totime * 0.001) #reset
    print ('next section at time: '+str(totime))
    session.player.seek(totime)
    oscsend('/key',track_data.key)
    oscsend('/majmin',track_data.maj_or_min)
    oscsend('/tempo',track_data.bpm)

# Register event listeners
session.on(
    spotify.SessionEvent.CONNECTION_STATE_UPDATED, on_connection_state_updated)
session.on(spotify.SessionEvent.END_OF_TRACK, on_end_of_track)

 # Block until Login is complete
print('Waiting for Login to Complete...')
session.login(spot_username, spot_password, remember_me=True)
logged_in.wait()
print('logged in!')

# Assuming a previous login with remember_me=True and a proper logout
#session.relogin()

#logged_in.wait()

# Play a track
tid = [ track_uri.split(':')[2] ]
print(tid)
track_data = get_analysis(tid)
section_times = track_data.section_times
print(section_times)
track = session.get_track(track_uri).load()
session.player.load(track)
session.player.play()
starttime = time.time()
current_segment = 0
segs = track_data.segments[0]
et = 0
pitchnames = ['c','c#','d','d#','e','f','f#','g','g#','a','a#','b']

# Wait for playback to complete or Ctrl+C or, better, Ctrl+Shift+\. There is probably a better way to do this.
try:
    while not end_of_track.wait(0.1):
        et = (time.time() - starttime) #elapsed time
        #print('tick %d',et)
        if segs[current_segment]['start'] < et:
            #get the segment pitches and filter out items with low presence (<0.7). Send list of 1/0 to pd
            pitchlist = segs[current_segment]['pitches']
            pitchbools = [int(x>0.8) for x in pitchlist]
            #print('pitchlist ' + str(segs[current_segment]['start'])+' -  '+str(pitchlist) )
            pitchchar = list()
            presentpitches = list()
            #massage the pitch array into something we can use in pure data. Instead of bools at note position, create a list of note numbers
            for p in range ( 0, len(pitchlist) ):
                if pitchbools[p] == 1:
                    presentpitches.append(p)
                    #pitchchar.append(pitchnames[p])
            oscsend('/pitches',presentpitches)
            #print('pitchchar ' + str(pitchchar) )
            current_segment = current_segment + 1
        if kb.kbhit():
            c = kb.getch()
            if ord(c) == 27: # ESC
                break
            if ord(c) == 110: # n
                to_next( timecount % len(section_times) )
                timecount = timecount+1
            if ord(c) == 115: # s
                print('s key')
        pass
except KeyboardInterrupt:
    pass
