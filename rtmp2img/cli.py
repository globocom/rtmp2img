import argparse
import logging
from lib import Shooter


def main():
    parser = argparse.ArgumentParser('Save images from live videos')
    parser.add_argument('--output', dest="output_file", help="path to output file", required=True)
    parser.add_argument('--url', dest="midia_url", help="rtmp url", required=True)

    parser.add_argument('--log', dest="log_path", help="log file path", default=None)

    parser.add_argument('--ffmpeg', dest='ffmpeg_bin', help='path to ffmpeg', default='ffmpeg')
    parser.add_argument('--rtmpdump', dest='rtmpdump_bin', help='path to rtmpdump', default='rtmpdump')

    args = parser.parse_args()

    logger = get_logger(args.log_path)
    shooter = Shooter(
        args.rtmpdump_bin,
        args.ffmpeg_bin,
        logger,)
    shooter.save_image(args.midia_url, args.output_file)


def get_logger(log_path):
    handler = logging.StreamHandler() if log_path is None else logging.FileHandler(log_path)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger("rtmp2img")
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


if __name__  == '__main__':
    main()