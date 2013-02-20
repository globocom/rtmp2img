rtmp2img
========

Simple way to save screenshots from rtmp live videos.


Usage
-----

Basic:

	$ rtmp2img --output /tmp/out.jpg --url rtmp://cp76072.live.edgefcs.net/live/MED-HQ-Flash@42814

With optional params:

	$ rtmp2img --ffmpeg /usr/local/bin/ffmpeg --rtmpdump /usr/local/bin/rtmpdump --output /tmp/out.jpg --url rtmp://cp76072.live.edgefcs.net/live/MED-HQ-Flash@42814 --log /tmp/test.log


Requirements
------------

OS requirements:
* ffmpeg
* rtmpdump

Python requirements:
Everything listed in requirements.txt