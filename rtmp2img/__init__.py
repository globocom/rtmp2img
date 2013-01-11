import tempfile
import os
import urlparse
import sh


class Shooter(object):

    def __init__(self, rtmpdump_bin, ffmpeg_bin, logger):
        self.rtmpdump_bin = rtmpdump_bin
        self.ffmpeg_bin = ffmpeg_bin
        self.logger = logger
        self.rtmpdump_defaults = {
            'stop_time': 1.0,
            'port': 1935
        }

    def get_url_params(self, url):
        url_parsed = urlparse.urlsplit(url)
        host = url_parsed.netloc
        path = url_parsed.path[1:]
        app, _, stream = path.rpartition('/')
        return (host, app, stream)

    def get_rtmpdump_command_args(self, url, output_file):
        host, app, stream = self.get_url_params(url)
        return ["--app", app,
                "--host", host,
                "--port", str(self.rtmpdump_defaults['port']),
                "--playpath", stream,
                "--stop", str(self.rtmpdump_defaults['stop_time']),
                "--live",
                "-o", output_file]

    def call_rtmpdump(self, url, output_file_path):
        args = self.get_rtmpdump_command_args(url, output_file_path)
        self.logger.debug('Calling rtmpdump %s', ' '.join(args))
        try:
            sh.Command(self.rtmpdump_bin)(args)
        except sh.ErrorReturnCode as e:
            self.logger.error("rtmpump FAILED!\n%s" % e.message)
            raise
        else:
            self.logger.debug("rtmpdump OK")


    def get_ffmpeg_command_args(self, input_file_path, output_file_path):
        return ['-i', input_file_path,
                '-vframes', '1',
                '-y', output_file_path]

    def call_ffmpeg(self, input_file_path, output_file_path):
        args = self.get_ffmpeg_command_args(input_file_path, output_file_path)
        self.logger.debug('Calling ffmpeg %s', ' '.join(args))
        try:
            sh.Command(self.ffmpeg_bin)(args)
        except sh.ErrorReturnCode as e:
            self.logger.error("ffmpeg FAILED!\n%s" % e.message)
            raise
        else:
            self.logger.debug('ffmpeg OK')

    def save_image(self, url, output_file_path):
        rtmpdump_temp_file = tempfile.mktemp()
        self.call_rtmpdump(url, rtmpdump_temp_file)
        try:
            self.call_ffmpeg(rtmpdump_temp_file, output_file_path)
        finally:
            os.remove(rtmpdump_temp_file)

