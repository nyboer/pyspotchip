# shows a user's playlists (need to be authenticated via oauth)

import sys
import spotipy
import spotipy.util as util

def show_tracks(tracks):
    print '==============='
    print tracks['items']
    print '==============='
    for i, item in enumerate(tracks['items']):
        track = item['track']
        output = u' '.join( (track['artists'][0]['name'], track['name'], track['uri']) ).encode('utf-8').strip()
        print '  '+str(i)+ ' ' +output


if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print "Whoops, need your username!"
        print "usage: python user_playlists.py [username]"
        sys.exit()

    token = util.prompt_for_user_token(username)

    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        pcount = len(playlists['items'])
        print 'Number of Playlists: ',str(pcount)
        for playlist in playlists['items']:
                print '-  -  -  -'
                print playlist['owner']['id']
                print playlist['name']
                print playlist['uri']
                print '  total tracks', playlist['tracks']['total']
                results = sp.user_playlist(username, playlist['id'],fields="tracks,next")
                tracks = results['tracks']
                print ' alt total: '+str(len(tracks['items']))
                show_tracks(tracks)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    show_tracks(tracks)
    else:
        print "Can't get token for", username
