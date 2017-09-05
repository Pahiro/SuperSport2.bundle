Unfortunately it seems that all of the DSTV streams are DRM enabled (should've suspected). FFMPEG transcoder doesn't support the SAMPLE-AES decryption yet (And it seems that most people expect that it likely won't ever). There are few libaries out there, of note; https://github.com/selsta/hlsdl, but I'm not quite sure how one would go about implementing it yet.

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
