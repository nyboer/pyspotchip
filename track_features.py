
# track analysis_url details at http://developer.echonest.com/docs/v4/_static/AnalyzeDocumentation.pdf
# shows acoustic features for tracks for the given artist

from __future__ import print_function    # (at top of module)
from spotipy.oauth2 import SpotifyClientCredentials
import json
import urllib
import spotipy
import time
import sys

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=True
#args = sys.argv

class track_data:
    section_times = list()
    segments = list()
    section_tempo = 120
    section_key = 0
    section_maj_or_min = 0
    tempo = 120
    key = 0
    maj_or_min = 0

def get_analysis(tracks):
    print(tracks)
    if len(tracks) > 0:
        section_times = list()
        tids = tracks[0:]
        count = len(tids)
        print('# of tracks: '+str(count) )

        start = time.time()
        features = sp.audio_features(tids)
        delta = time.time() - start
        print (">>features retrieved in %.2f seconds" % (delta,))
        #keys:
        for v in features[0]:
            print (v)

        track_data.key = features[0]['key']
        track_data.maj_or_min = features[0]['mode']
        track_data.bpm = features[0]['tempo']

        print ('---track analysis_url---')
        #fetch data from the returned object:
        for i in range( 0,count ):
            print(features[i]['analysis_url'])
        url = features[i]['analysis_url']
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        #add section start times to list
        section_count = len( data['sections'] )
        track_data.segments.append(data['segments'])
        #print('--section data--'+str(section_count))
        for v in range(0,section_count):
            starttime = data['sections'][v]['start']
            track_data.section_times.append(starttime)
            tempo = data['sections'][v]['tempo']
            track_data.section_tempo = tempo
            key = data['sections'][v]['key']
            track_data.section_key = key

        return track_data
