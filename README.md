08-Sept-2017

Selsta highlighted to me that each of the manifests generated through USP are DRM enabled and as a result, can't be transcoded into anything, nor would Plex be able to direct play the content. If Plex ever got around to supporting DRM enabled content, which seems unlikely, this could be something to look at again. 

My intention with this was not and will never be to provide illegal access to DRM protected content but was an attempt to provide an alternative player for Supersport content. To centralize my media consumption to Plex, as it's what I use for just about everything else. Was hoping to flesh out this channel with an EPG eventually as well.

PS. DSTV uses Google's Widevine DRM protection. If you spot something in Plex's updates referencing Widevine, let me know. :)

07-Sept-2017

Looked into Unified Streaming Platform

Available formats listed:
- MPD (MPEG Dash)
- M3U8 (HTTP Live Streaming)
- F4M (HDS - HTTP Dynamic Streaming)
- Manifest (Smooth Streaming)

Results of current tests:
- MPD - FFMPEG: Invalid data found when processing input
- M3U8 - FFMPEG: SAMPLE-AES encryption is not supported yet
- F4M - Server responds with 403: Access Denied
- Manifest - FFMPEG: Invalid data found when processing input

I suspect I just need to properly specify a protocol for the Manifest and MPD. Looking into it.

06-Sept-2017

Spoke to Selsta and he stated that he's not planning on implementing SAMPLE-AES into FFMPEG directly any time soon and I looked at the code, it's mind-numbingly complex so I'm not even going to try that.

05-Sept-2017

M3U8 - Transcoding fails. FFMPEG: SAMPLE-AES encryption is not supported yet
