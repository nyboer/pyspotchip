
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
spc = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
spc.trace=False
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
        track_data.section_times = list()
        track_data.segments = list()
        tids = tracks[0:]
        count = len(tids)
        start = time.time()
        features = spc.audio_features(tids)
        delta = time.time() - start
        print (">>features retrieved in %.2f seconds" % (delta,))

        # print keys to dict:
        # for v in features[0]:
        #     print (v)

        track_data.key = features[0]['key']
        track_data.maj_or_min = features[0]['mode']
        track_data.bpm = features[0]['tempo']

        print ('---track analysis_url---')
        #fetch data from the returned object:
        for i in range( 0,count ):
            print(features[i]['analysis_url'])
        try:
            analysis = spc._get(features[i]['analysis_url'])
            #print(json.dumps(analysis, indent=4))
            #add section start times to list
            section_count = len( analysis['sections'] )
            track_data.segments.append(analysis['segments'])
            #print('--section data--'+str(section_count))
            for v in range(0,section_count):
                starttime = analysis['sections'][v]['start']
                track_data.section_times.append(starttime)
                tempo = analysis['sections'][v]['tempo']
                track_data.section_tempo = tempo
                key = analysis['sections'][v]['key']
                track_data.section_key = key
        # if there's no analysis data, we'll make some
        except:
            section_count = 10
            defdata = [0,1000,2000,3000,4000,5000,6000,7000,8000,9000]
            track_data.segments.append(defdata)
            track_data.section_times.append(0)
            track_data.section_tempo = 120
            track_data.section_key = 0

        return track_data
