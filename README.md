This plugin is not yet fully functional.

SuperSport2.bundle
=================
SuperSport video plugin for Plex

Information:
============
This plug in will eventually allow you to watch live sports streams and highlighs packages from the SuperSport website.

In order to watch live streams you must enter your login details that are linked to your smartcard.

Enjoy!

Known Issues:
=============
Time-out on Channel during login process (DSTV's login page is slow). Looking into async thread with callback to populate session.

Currently no service to play DASH MPEG in Plex. Looking into the different containers. DSTV uses Bitmovin container. Stream URL responds with ISML file. Bitmovin requires either MPD or M3U8 file. If you append .m3u8 to the url it generates a playlist automatically. Not sure what this means or if it'll help in any way. First things first is getting a generic MPD file to play in plex.

Instructions:
=============

1. To add this plugin to Plex copy this .bundle folder to your PlexMediaServer plug-ins folder.

Thanks:
=======
This plugin is based off an older version which was written by drzoidberg33
