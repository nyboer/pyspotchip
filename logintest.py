import spotify
import threading
from creds import spot_password spot_username

def on_connection_state_updated(session):
    if session.connection.state is spotify.ConnectionState.LOGGED_IN:
        print 'callback: logged in'
        logged_in.set()

# Events for coordination
logged_in = threading.Event()

config = spotify.Config()
config.user_agent = 'My Spotify client'
config.tracefile = b'/tmp/libspotify-trace.log'

session = spotify.Session(config)

# Process events in the background
loop = spotify.EventLoop(session)
loop.start()

# Register event listeners
session.on(spotify.SessionEvent.CONNECTION_STATE_UPDATED, on_connection_state_updated)

session.login(spot_username,spot_password)
print 'waiting...'
logged_in.wait()
print 'done waiting...'
print session.connection.state
