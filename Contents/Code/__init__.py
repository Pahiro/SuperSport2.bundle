####################################################################################################
import re
import pyaes
import urllib, urllib2, json
import auth
import httplib
import requests

VIDEO_PREFIX = "/video/SuperSport2"

NAME = "SuperSport2 Plugin"

LIVE_STREAMS_URL = "https://www.supersport.com/AjaxOperation.aspx/GetVideoStreams"
HIGHLIGHTS_URL = "https://www.supersport.com/%s"
LIVE_DATA_WS_URL = "https://www.supersport.com/video/dataLive.aspx"
LIVE_DATA_JSON_URL = "https://www.supersport.com/video/playerlivejson.aspx"
VIDEO_DATA_WS_URL = "https://www.supersport.com/video/data.aspx"
VIDEO_DATA_JSON_URL = "https://www.supersport.com/video/playerjson.aspx"
SWF_PLAYER_URL_OLD = "https://core.dstv.com/video/flash/DSTV_VideoPlayer.swf?v=1-15"
SWF_PLAYER_URL = "https://core.dstv.com/video/flash/PlayerDStv.swf?v=2"

ART = 'art-default.jpg'
ICON = 'icon-default.png'

####################################################################################################

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

####################################################################################################

def MainMenu():

	oc = ObjectContainer()  

	oc.add(DirectoryObject(key = Callback(LiveStreamMenu), title = 'Live Streams'))
	#oc.add(DirectoryObject(key = Callback(HighlightsMenu), title = 'Highlights'))

	oc.add(PrefsObject(title = L('Preferences')))

	return oc

####################################################################################################

def LiveStreamMenu():
	Log("auth level = %s" % auth.check_auth())
	cookie = auth.check_auth()
	if cookie == False:
		cookie = auth.login()
	
	if cookie != False:
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
	

	r = requests.get(LIVE_STREAMS_URL, headers=headers)

	live_stream_data = json.loads(r.text)
	
	for live_streams in live_stream_data['d']['ChannelStream']:
		live_streams_str = live_streams['NowPlaying']['Link']
		
		live_streams_id = (re.findall('https://www.supersport.com/live-video/([0-9]{1,6})', live_streams_str))[0]
		live_streams_json_query = LIVE_DATA_JSON_URL + "?vid=" + live_streams_id
		
		r = requests.get(live_streams_json_query, headers=headers, cookies=cookie)
		#Getting a freaking Auth fail here. Works in browser.
		#channel_data = json.loads(r.text)
		
		Log("Stream found: " + live_streams['NowPlaying']['Channel'] + ": " + live_streams_id)
		
		oc.add(VideoClipObject(
			key = RTMPVideoURL(
				url = live_streams['NowPlaying']['Link'], #channel_data['result']['services']['videoURL'],
				clip = live_streams['NowPlaying']['Link'],
				swf_url = SWF_PLAYER_URL, 
				live = True),
				rating_key = live_streams_id,
				#thumb = Resource.ContentsOfURLWithFallback(url=channel_data['result']['menu']['details']['imageURL'], fallback=ICON), 
				title = live_streams['NowPlaying']['Channel'],
				summary = live_streams['NowPlaying']['EventNowPlaying'] 
				)
			)
	return oc
