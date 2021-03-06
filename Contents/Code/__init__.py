import re
import pyaes
import urllib, urllib2, json
import auth
import httplib
import requests
import cookielib
import os


VIDEO_PREFIX = "/video/SuperSport2"
NAME = "SuperSport2 Plugin"
LIVE_STREAMS_URL = "https://www.supersport.com/AjaxOperation.aspx/GetVideoStreams"
LIVE_DATA_JSON_URL = "https://www.supersport.com/video/playerlivejson.aspx"
RAW_HLS_CLIENTS = ['Android', 'iOS', 'Roku', 'Safari', 'tvOS', 'Mystery 4', 'Konvergo']
ART = 'art-default.jpg'
ICON = 'icon.png'

session = auth.session

if auth.token == None:
	auth.login()
	session = auth.session
else:
	Log(auth.token)

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
	global session
	url = url.split('?',1)[0]
	Log(url)
	######################################
	# Unified Streaming Platform formats #
	######################################
	#hls_url = url.replace('.isml','.isml/playlist.m3u8') #FFMPEG: SAMPLE-AES encryption is not supported yet
	#hls_url = url.replace('.isml','.isml/.mpd') #FFMPEG: Invalid data found when processing input
	hls_url = url.replace('.isml','.isml/Manifest') #FFMPEG: Invalid data found when processing input
	#hls_url = url.replace('.isml','.isml/.f4m') #403 Forbidden
	
	r = session.get(hls_url)
	f = os.open('print.txt', os.O_WRONLY + os.O_CREAT)
	os.write(f, r.text)
	os.close(f)	

	return [
        MediaObject(
            parts = [
                PartObject(
					key=HTTPLiveStreamURL(Callback(PlayHLS, url=hls_url))
                	#PartObject(key=Callback(PlayHLS, url=hls_url))
                 	#PartObject(key=HTTPLiveStreamURL(hls_url))
                )
            ],
			protocol = 'hss',
			container = 'mp4',
			video_codec = 'avc',
			audio_codec = 'aac',
            video_resolution = 720,
            audio_channels = 2,
            video_frame_rate = 50,
            optimized_for_streaming = True
        )
    ]

@indirect
@route(VIDEO_PREFIX + '/playhls.m3u8')
def PlayHLS(url):
	global session
	return IndirectResponse(VideoClipObject, key=url, http_cookies=str(session.cookies))