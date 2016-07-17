# pyspotchip
python and libspotify and Spotify Web API on CHIP

## Pyspotify

install libspotify for Debian. Instructions [here](https://github.com/mopidy/libspotify-deb)

requires [pyspotify](https://github.com/mopidy/pyspotify). 

Install pyspotify [instructions](http://pyspotify.readthedocs.io/en/latest/installation/)

Setup pyspotify [quickstart](https://pyspotify.mopidy.com/en/latest/quickstart/) including instructions on getting and placing `spotify_appkey.key`.

You'll need Spotify login info to use libspotify. If you want to use the twitter API, you'll need keys for that.
Create a document with all of these called "creds.py"
```
spot_username = 'spotify username'
spot_password = 'secret password'
twit_consumer_key = 'erreU[...]3cuno'
twit_consumer_secret = 'w30bf[...]aDPYVm'
twit_access_token_key = '22228[...]lvE1EW'
twit_access_token_secret ='rbI[...]RJ4'
```
This way, you can just import these variables as a python module and use them in your scripts.

## Spotipy

requires [spotipy](https://github.com/plamere/spotipy). 
Install spotipy [instructions](http://spotipy.readthedocs.io/en/latest/#)


The spotipy API needs your Spotify API keys,
and you'll need to set environment variables so spotipy calls can get them.
You can do this with a script that you call using `source`. Make `spotcreds.sh` and add content like so:
```
export SPOTIPY_CLIENT_ID='f6b5e0293b1446fbbd9402c1f365085e'
export SPOTIPY_CLIENT_SECRET='ec56c12525ce49fbb19f442e0916a52b'
export SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'
export LD_LIBRARY_PATH=/usr/local/lib
```
(the last line is for pyliblo, but you might as well put it in there).

## OSC

for OSC to work, I'm trying [pyliblo](http://das.nasophon.de/pyliblo/). This requires Cython and liblo, and should work with vanilla PD

```
cd ~/Documents
sudo apt-get install autoconf libtool automake
sudo pip install Cython
git clone https://github.com/radarsat1/liblo/blob/master/INSTALL
cd liblo
./autogen.sh 
make
sudo make install
cd ~/Documents
git clone https://github.com/dsacre/pyliblo
cd pyliblo
./setup.py build
sudo ./setup.py install
export LD_LIBRARY_PATH=/usr/local/lib
```

The last line lets python find liblo, which is installed in /usr/local/lib on `make install`


another OSC option would be [pyosc](https://github.com/ptone/pyosc). This requires externals that are not part of PD Vanilla, so it's second class.


### In Brief:
To install libspotify, pyspotify, and spotipy:

```
sudo apt-get update
wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
sudo wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/jessie.list
sudo sed -i '$ a # Mopidy APT archive\ndeb http://apt.mopidy.com/ stable main contrib non-free\ndeb-src http://apt.mopidy.com/ stable main contrib non-free' /etc/apt/sources.list
sudo apt-get update
sudo apt-get install -y build-essential libspotify12 libspotify-dev  python-dev python-spotify python-pip python-alsaaudio libasound2-dev
sudo pip install spotipy setuptools 
```

For pyspotify, you'll need to get your spotify app key (binary version) from your [spotify developer account](https://devaccount.spotify.com/my-account/keys/) and put "spotify_appkey.key" into the same directory as the python scripts you are using.

For spotipy (Web API), you'll also need a file called *creds.py* with the necessary login info to your paid account, like:

```
spot_username = 'username'
spot_password = 'secretpassword'
```

## The Files

There are a variety of experiments and examples littering this repository. Here's some notes on the different ideas in each:

### Python Modules
  * creds.py - Ignored by repo. This has keys and passwords that a script can import
  * keys.py - Listens for keyboard key presses so we can use a keyboard as action buttons.
  * osc_tx.py - Simple module to send OSC messages from a python script
  * track_features.py - Makes calls to Spotify Web API to get track features and analysis data

### Python Scripts
  * audio_features_for_track.py - Call with a spotify track ID as argument. An example that shows how to get feature information for a track.
  * example_OSCclient.py - pyliblo example on how to send Open Sound Control messages from python
  * pd_rx_OSC.py.pd - Companion Pure Data patch to receive OSC messages
  * play_analysis.py - Example using Spotify Web API to get analysis info for the playing track. It creates a "smart fast forward" and getting note data for each segment to create an auto-accompaniment, sending OSC notes to a synthesizer 
  * play_analysis.sh - ignored. A script to run play_analysis.py by setting up credentials as environment variables, then calling the python script.
  * play_list.py - Plays a Spotify Playlist. Several features can be triggered with keys on keyboard. This is the main result of the experiments so far!
  * play_list.sh - ignored. A script to run play_analysis.py by setting up
  * play_track.py - Example of using pyspotify (libspotify) to play a track from Spotify
  * shell.py - Example of a commandline client for Spotify. good reference.
  * spotify_appkey.key - ignored. You'll need this for spotipy Web API access
  * tweet.py - ignored. For sending message to twitter. Could be useful someday.
  * twit_init.py - ignored. For sending message to twitter

