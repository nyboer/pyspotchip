

# shows acoustic features for tracks for the given track

from __future__ import print_function    # (at top of module)
from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
import time
import sys


client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=True

if len(sys.argv) > 1:
    tids = sys.argv[1:]
    count = len(tids)
    print('# of tracks: '+str(count) )

    start = time.time()
    features = sp.audio_features(tids)
    delta = time.time() - start
    features_data = json.dumps(features)
    print (">>features retrieved in %.2f seconds" % (delta,))
    #keys:
    for v in features[0]:
        print (v)
    print ('---track uris---')
    #fetch data from the returned object:
    for i in range( 0,count ):
        print(features[i]['uri'])
