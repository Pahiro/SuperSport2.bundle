import re
import pyaes
import urllib, urllib2, json
import auth
import httplib
import requests
import cookielib

VIDEO_PREFIX = "/video/SuperSport2"
NAME = "SuperSport2 Plugin"
LIVE_STREAMS_URL = "https://www.supersport.com/AjaxOperation.aspx/GetVideoStreams"
LIVE_DATA_JSON_URL = "https://www.supersport.com/video/playerlivejson.aspx"
RAW_HLS_CLIENTS = ['Android', 'iOS', 'Roku', 'Safari', 'tvOS', 'Mystery 4', 'Konvergo']
ART = 'art-default.jpg'
ICON = 'icon.png'

session = auth.session

try:
	#Check whether we have our cookie in memory
	#Need to store this in a file. Channel is logging in too often.
	session.cookies['connectIdCookie']
except:
	auth.login()
	session = auth.session

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

@handler(VIDEO_PREFIX, "SuperSport2", thumb=ICON)
def MainMenu():
	oc = ObjectContainer()  

	oc.add(DirectoryObject(key = Callback(LiveStreamMenu), title = 'Live Streams'))
	#oc.add(DirectoryObject(key = Callback(HighlightsMenu), title = 'Highlights'))

	oc.add(PrefsObject(title = L('Preferences')))

	return oc

@route(VIDEO_PREFIX + '/highlights')
def HighlightsMenu():
	oc = ObjectContainer(title2 = "Highlights", view_group= "InfoList")
	return oc

@route(VIDEO_PREFIX + '/livestreams')
def LiveStreamMenu():	
	global session
	
	oc = ObjectContainer(title2 = "Live Streams", view_group= "InfoList")

	headers = { 'Content-Type' : 'application/json; charset=utf-8' }
	r = session.get(LIVE_STREAMS_URL, headers=headers)
	Log(r.status_code)
	live_streams = json.loads(r.text)
	
	for index, live_stream in enumerate(live_streams['d']['ChannelStream']):
		live_stream_url = live_stream['NowPlaying']['Link']
		live_stream_id = (re.findall('https://www.supersport.com/live-video/([0-9]{1,6})', live_stream_url))[0]
		live_stream_json = LIVE_DATA_JSON_URL + "?vid=" + live_stream_id
		live_stream_title = live_stream['NowPlaying']['Channel']
		live_stream_summary = live_stream['NowPlaying']['EventNowPlaying'] 
		
		r = session.get(live_stream_json)
		channel_data = json.loads(r.text)
		
		live_stream_m3u8 = channel_data['result']['services']['videoURL']
		
		oc.add(CreateVideoClipObject(
				stream_id = live_stream_id,
				stream_title = live_stream_title,
				stream_url = live_stream_m3u8,
				stream_summary = live_stream_summary
			)
		)
	return oc

@route(VIDEO_PREFIX + '/createvideoclipobject', include_container=bool)
def CreateVideoClipObject(stream_id, stream_title, stream_url, stream_summary, include_container=False, **kwargs):
	videoclip_obj = VideoClipObject(
		key = Callback(CreateVideoClipObject,
					stream_id = stream_id,
					stream_title = stream_title,
					stream_url = stream_url,
					stream_summary = stream_summary,
					include_container=True),
		rating_key = stream_id,
		title = stream_title,
		items = MediaObjectsForURL(stream_url),
		thumb = R('icon' + stream_title + '.png'),
		art = R(stream_title + '.jpg'),		
		summary = stream_summary
	)

	if include_container:
		return ObjectContainer(objects=[videoclip_obj])
	else:
		return videoclip_obj

@deferred
def MediaObjectsForURL(url):
	#Original is an ISML playlist. 
	hls_url = url.replace('.isml','.isml/playlist.m3u8') 
	
	streams = GetHLSStreams(hls_url)

	if Client.Platform in RAW_HLS_CLIENTS:
		return [
            MediaObject(
                parts = [
					PartObject(key=HTTPLiveStreamURL(hls_url))
                    #PartObject(key=Callback(PlayHLS(hls_url)))
                ],
                video_resolution = 720,
				protocol='dash',
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
		mo.append(
            MediaObject(
                parts = [
                    PartObject(
						#key = HTTPLiveStreamURL(Callback(PlayHLS,url=stream['url']))
						key = HTTPLiveStreamURL(url=stream['url'])
					)
                ],
                video_resolution = stream['resolution'],
                protocol='dash',
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

@indirect
def PlayHLS(url):
	return IndirectResponse(VideoClipObject, key=HTTPLiveStreamURL(url))