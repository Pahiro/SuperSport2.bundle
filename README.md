08-Sept-2017

Selsta highlighted to me that each of the streams generated through USP are DRM enabled and as a result, can't be transcoded into anything, nor would Plex be able to direct play the content. Seems that DRM locks the content to a specific player, which in this case is the Bitmovin player.

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
