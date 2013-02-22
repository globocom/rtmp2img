import logging
import os
import tempfile
from rtmp2img import Shooter


here = os.path.dirname(os.path.abspath(__file__))
TESTS_DATA = os.path.join(here, 'data')


def create_logger():
    handler = logging.FileHandler(os.path.join(here, 'logs', 'test.log'))
    formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger("test Shooter")
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


logger = create_logger()


class FakeShooter(Shooter):
    def get_ffmpeg_extra_args(self):
        return ['-loglevel', 'debug']


test_shooter_args = {
    'logger': logger,
    'ffmpeg_bin': 'ffmpeg',
    'rtmpdump_bin': 'rtmpdump',
}

# got from: http://www.nasa.gov/multimedia/nasatv/media_flash.html
NASA_TV_URL = 'rtmp://cp76072.live.edgefcs.net/live/MED-HQ-Flash@42814'
LIVE_RTMP_URL = NASA_TV_URL


def test_get_url_params_should_work_for_flash_media_server_rtmp_style_urls():
    url = 'rtmp://anyserver.com/app/inst/stream'
    shooter = Shooter(**test_shooter_args)
    assert shooter.get_url_params(url) == ('anyserver.com', 'app/inst', 'stream')


def test_get_url_params_should_work_for_wowza_server_rtmp_style_urls():
    url = 'rtmp://anyserver.com/app/stream'
    shooter = Shooter(**test_shooter_args)
    assert shooter.get_url_params(url) == ('anyserver.com', 'app', 'stream')


def test_rtmpdump_command_args_with_simple_stream_url():
    url = 'rtmp://anyserver.com/app/inst/stream'

    shooter = Shooter(**test_shooter_args)
    result = shooter.get_rtmpdump_command_args(url, '/path/to/output.flv')

    assert result == ["--app", 'app/inst',
                      "--host", 'anyserver.com',
                      "--port", '1935',
                      "--playpath", 'stream',
                      "--stop", '1.0',
                      "--live",
                      "-o", "/path/to/output.flv"]


def test_call_rtmpdump_should_create_a_flv_file_if_stream_exists(tmpdir):
    url = LIVE_RTMP_URL
    output_file_path = str(tmpdir.join('out.flv'))
    
    shooter = Shooter(**test_shooter_args)
    shooter.call_rtmpdump(url, output_file_path)

    assert tmpdir.listdir() == [output_file_path]
    assert os.stat(output_file_path).st_size > 0, "rtmdump output FLV is broken"


def test_ffmpeg_command_args():
    shooter = Shooter(**test_shooter_args)

    result = shooter.get_ffmpeg_command_args('/path/to/rtmpdump/output.flv', '/path/to/image.jpg')

    assert result == ['-i', '/path/to/rtmpdump/output.flv',
                      '-vframes', '1',
                      '-y', '/path/to/image.jpg']

def test_ffmpeg_extra_args():
    shooter = FakeShooter(**test_shooter_args)

    result = shooter.get_ffmpeg_command_args('/path/to/rtmpdump/output.flv', '/path/to/image.jpg')

    assert result == ['-i', '/path/to/rtmpdump/output.flv',
                      '-vframes', '1',
                      '-loglevel', 'debug',
                      '-y', '/path/to/image.jpg']


def test_call_ffmpeg_should_create_a_jpg_file(tmpdir):
    input_file_path = os.path.join(TESTS_DATA, 'video.flv')
    output_file_path = str(tmpdir.join('out.jpg'))
    
    shooter = Shooter(**test_shooter_args)
    shooter.call_ffmpeg(input_file_path, output_file_path)

    assert tmpdir.listdir() == [output_file_path]
    assert os.stat(output_file_path).st_size > 0, "ffmpeg output JPG is broken"


def test_save_image_should_only_save_jpg(tmpdir):
    url = LIVE_RTMP_URL
    output_file_path = str(tmpdir.join('out.jpg'))

    shooter = Shooter(**test_shooter_args)
    shooter.save_image(url, output_file_path)

    assert tmpdir.listdir() == [output_file_path]
    assert os.stat(output_file_path).st_size > 0, "output JPG is broken"


def test_save_image_should_discard_rtmpdump_temp_file(monkeypatch, tmpdir):
    url = LIVE_RTMP_URL
    output_file_path = str(tmpdir.join('out.jpg'))

    def mktemp_mock():
        return str(tmpdir.join('out.flv'))
   
    monkeypatch.setattr(tempfile, 'mktemp', mktemp_mock)
   
    shooter = Shooter(**test_shooter_args)
    shooter.save_image(url, output_file_path)

    assert tmpdir.listdir() == [output_file_path]


def test_save_image_should_not_create_rtmpdump_temp_file_if_rtmpdump_fail(monkeypatch, tmpdir):
    url = LIVE_RTMP_URL + '-NOTFOUND'
    output_file_path = str(tmpdir.join('out.jpg'))

    def mktemp_mock():
        return str(tmpdir.join('out.flv'))

    monkeypatch.setattr(tempfile, 'mktemp', mktemp_mock)

    shooter = Shooter(**test_shooter_args)
    try:
        shooter.save_image(url, output_file_path)
        assert False, "ffmpeg should raise an exception because FLV is broken"
    except:
        pass

    assert tmpdir.listdir() == []

def test_save_image_should_work_with_rtmpdump_temp_file_param(tmpdir):
    url = LIVE_RTMP_URL
    output_file_path = str(tmpdir.join('out.jpg'))
    temp_file_path = str(tmpdir.join('temp.flv'))

    shooter = Shooter(**test_shooter_args)
    shooter.save_image(url, output_file_path, temp_file_path)

    assert os.stat(output_file_path).st_size > 0, "output JPG is broken"
