import re
import pyaes
import urllib, urllib2, json
import auth
import httplib
import requests
import cookielib

Log("Initializing...")

session = auth.session

try:
	session.cookies['connectIdCookie']
except:
	auth.login()
	session = auth.session

VIDEO_PREFIX = "/video/SuperSport2"

NAME = "SuperSport2 Plugin"

LIVE_STREAMS_URL = "https://www.supersport.com/AjaxOperation.aspx/GetVideoStreams"
LIVE_DATA_JSON_URL = "https://www.supersport.com/video/playerlivejson.aspx"
VIDEO_DATA_WS_URL = "https://www.supersport.com/video/data.aspx"
VIDEO_DATA_JSON_URL = "https://www.supersport.com/video/playerjson.aspx"

RAW_HLS_CLIENTS = ['Android', 'iOS', 'Roku', 'Safari', 'tvOS', 'Mystery 4', 'Konvergo']

ART = 'art-default.jpg'
ICON = 'icon-default.png'

def Start():
	Plugin.AddPrefixHandler("/video/SuperSport2", MainMenu, "SuperSport2", ICON, ART)
	Plugin.AddViewGroup("InfoList", viewMode = "InfoList", mediaType = "items")
	Plugin.AddViewGroup("List", viewMode = "List", mediaType = "items")
	ObjectContainer.title1 = "SuperSport2"
	ObjectContainer.art = R(ART)
	ObjectContainer.view_group = 'List'
	DirectoryObject.thumb = R(ICON)
	DirectoryObject.art = R(ART)
	VideoClipObject.thumb = R(ICON)

def MainMenu():
	global session
	session = auth.session #Our global session
	
	Log("Logging in...")
	
		
	oc = ObjectContainer()  

	oc.add(DirectoryObject(key = Callback(LiveStreamMenu), title = 'Live Streams'))
	#oc.add(DirectoryObject(key = Callback(HighlightsMenu), title = 'Highlights'))

	oc.add(PrefsObject(title = L('Preferences')))

	return oc

def LiveStreamMenu(*args, **kwargs):	
	global session
	session = auth.session #Our global session
	
	if session != None:
		oc = ObjectContainer(title2 = "Live Streams", view_group= "InfoList")
	
		headers = { 'Host' : 'www.supersport.com', 
				    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
					'Accept' : '*/*',
					'Accept-Language' : 'en-US,en;q=0.5',
					'Accept-Encoding' : 'gzip, deflate, br',
					'Content-Type' : 'application/json; charset=utf-8',
					'X-Requested-With' : 'XMLHttpRequest',
					'Referer' : 'https://www.supersport.com/live-video',
					'Connection' : 'keep-alive',
					'Pragma' : 'no-cache',
					'Cache-Control' : 'no-cache' }
	

	r = session.get(LIVE_STREAMS_URL, headers=headers)

	live_stream_data = json.loads(r.text)
	
	for index, live_streams in enumerate(live_stream_data['d']['ChannelStream']):
		live_streams_str = live_streams['NowPlaying']['Link']
		
		live_streams_id = (re.findall('https://www.supersport.com/live-video/([0-9]{1,6})', live_streams_str))[0]
		live_streams_json_query = LIVE_DATA_JSON_URL + "?vid=" + live_streams_id
		
		r = session.get(live_streams_json_query, headers=headers)
		
		try:
			channel_data = json.loads(r.text)
		except:
			Log(r.reason + ": Authorization failed - Close all sessions and try again")
			channel_data = None #Authorization Failed
			
		if channel_data != None:
			Log("Stream found: " + live_streams['NowPlaying']['Channel'] + ": " + live_streams_id)
			Log("Stream URL: " + channel_data['result']['services']['videoURL'])
			
			items = MediaObjectsForURL(channel_data['result']['services']['videoURL'])
			Log("Adding video clips")
			if items != None and live_streams_id != None:
				oc.add(
					VideoClipObject(
						key = live_streams_id,
						rating_key = live_streams_id,
						title = live_streams['NowPlaying']['Channel'],
						items = items,
						thumb = Resource.ContentsOfURLWithFallback(url=channel_data['result']['menu']['details']['imageURL'], fallback=ICON),
						art = Resource.ContentsOfURLWithFallback(url=channel_data['result']['menu']['details']['imageURL'], fallback=ICON),
						summary = live_streams['NowPlaying']['EventNowPlaying']
					)
			)
			if index == 1:
				break
	return oc

@indirect
def PlayHLS(url):
	return IndirectResponse(VideoClipObject, key=HTTPLiveStreamURL(url))

@deferred
def MediaObjectsForURL(url):
	hls_url = url.replace('.isml','.isml/playlist.m3u8') 
	
	streams = GetHLSStreams(hls_url)

	if Client.Platform in RAW_HLS_CLIENTS:
		return [
            MediaObject(
                parts = [
                    PartObject(key=Callback(PlayHLS(hls_url)))
                ],
                video_resolution = 720,
				protocol='hls',
				container='mpegts',
				video_codec=VideoCodec.H264,
				audio_codec=AudioCodec.AAC,
                audio_channels = 2,
                video_frame_rate = 50,
                optimized_for_streaming = True
            )
        ]

	mo = []
	Log("Constructing Media Objects")
	for stream in streams:
		Log(stream['url'])
		#r = session.get(stream['url'])
		#Log(r.reason + ":" + r.text)
		mo.append(
            MediaObject(
                parts = [
                    PartObject(
						key = HTTPLiveStreamURL(Callback(PlayHLS,url=stream['url']))
					)
                ],
                video_resolution = stream['resolution'],
                protocol='hls',
                container='mpegts',
                video_codec=VideoCodec.H264,
				audio_codec=AudioCodec.AAC,
                audio_channels = 2,
                video_frame_rate = 50 if stream['resolution'] == 720 else 25,
                bitrate = int(stream['bitrate'] / 1024),
                optimized_for_streaming = True
            )
		)
	Log("Return Media Items")
	return mo


def GetHLSStreams(url):
	global session
	
	streams = []

	r = session.get(url)
	playlist = r.text

	# Parse the m3u8 file to get:
	# - URL
	# - Resolution
	# - Bitrate
	for line in playlist.splitlines():
		if 'BANDWIDTH' in line:
			stream = {}
			stream['bitrate'] = int(Regex('(?<=BANDWIDTH=)[0-9]+').search(line).group(0))

			if 'RESOLUTION' in line:
				stream['resolution'] = int(Regex('(?<=RESOLUTION=)[0-9]+x[0-9]+').search(line).group(0).split('x')[1])
			else:
				stream['resolution'] = 0

		elif '.m3u8' in line:
			path = ''

			if not line.startswith('http'):
				path = url[ : url.rfind('/') + 1]

			stream['url'] = path + line

			streams.append(stream)

	sorted_streams = sorted(streams, key=lambda stream: stream['bitrate'], reverse=True)

	return sorted_streams