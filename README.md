Unfortunately it seems that all of the DSTV streams are DRM enabled. FFMPEG transcoder doesn't support the SAMPLE-AES decryption yet. At least this plugin is ready for the day that happens. There are few libaries out there, of note; https://github.com/selsta/hlsdl, but I'm not quite sure how one would go about implementing it yet. 

Spoke to Selsta and he stated that he's not planning on implementing SAMPLE-AES into FFMPEG directly any time soon and I looked at the code, it's mind-numbingly complex so I'm not even going to try that.

Looking into .MPD as an alternative to the .M3U8 (which was intended for Apple). The Bitmovin player on now.dstv.com & supersport.com utilizes .MPD. At the moment with Direct Play on I get a 400 (Bad-request) response code from the transcoder and with it off I get a 404 (Not found). Might need to reformat the stream URLs. Still worried that the .ts files the MPD points to are going to be SAMPLE-AES encrypted as well but we'll see.

SuperSport2.bundle
=================
SuperSport video plugin for Plex

Information:
============
This plug in will allow you to watch live sports streams and highlighs packages from the SuperSport website. 

Known Issues:
=============
[Transcoder] [hls,applehttp] SAMPLE-AES encryption is not supported yet

Instructions:
=============
1. To add this plugin to Plex copy this .bundle folder to your PlexMediaServer plug-ins folder.

Thanks:
=======
This plugin is based off an older version which was written by drzoidberg33
