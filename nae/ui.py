import argparse
from .database_handle import NaeDatabase
from .webui import WebUI
from .file_handle import FileHandle
from .default_config import NaeConfig
import uvicorn


def import_media(media_path, test, config: NaeConfig):
    db = NaeDatabase(config=config)
    fh = FileHandle(media_path_to_import=media_path,
                    keep_original_file=config.KEEP_ORIGINAL_FILE,
                    link=False,
                    handle_files=True,
                    database=db,
                    config=config)

    fh.import_media(test=test)


def serve(config: NaeConfig):
    webui = WebUI(config=config)
    uvicorn.run(webui.app, host="127.0.0.1", port=config.PORT, reload=False)


class Args2Config:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="A simple music organizer.")
        self.subparsers = self.parser.add_subparsers(
            dest='command', required=True)

        self.regsist_check_parser()
        self.regsist_serve_parser()
        self.regsist_import_parser()

    def regsist_check_parser(self):
        check_parser = self.subparsers.add_parser(
            'check', help='Check if media tags is complete.')
        check_parser.add_argument(
            '--path', nargs='?',
            help='The path of the media file.',
            default='.')
        self.add_config_arguments(check_parser)

    def regsist_import_parser(self):
        import_parser = self.subparsers.add_parser(
            'import', help='Import media files.')
        import_parser.add_argument(
            '--path', nargs='?',
            help='The path of the media file.',
            default='.')
        self.add_config_arguments(import_parser)

    def regsist_serve_parser(self):
        serve_parser = self.subparsers.add_parser(
            'serve', help='Serve the web UI.')
        self.add_config_arguments(serve_parser)

    def add_config_arguments(self, parser):
        default_config = NaeConfig()
        parser.add_argument(
            '--base_dir', nargs='?', default=default_config.BASE_DIR,
            help='The base directory of the nae music library')
        parser.add_argument(
            '--port', nargs='?', default=default_config.PORT,
            help='The port number.')
        parser.add_argument(
            '--keep_original_file', nargs='?',
            default=default_config.KEEP_ORIGINAL_FILE,
            help='Keep the original file.')

    def get_config(self) -> NaeConfig:
        args = self.parser.parse_args()
        print(args.port)
        if type(args.keep_original_file) is str:
            args.keep_original_file = eval(args.keep_original_file)
        if type(args.port) is str:
            args.port = eval(args.port)
        return NaeConfig(
            BASE_DIR=args.base_dir,
            PORT=args.port,
            KEEP_ORIGINAL_FILE=args.keep_original_file)


def main():
    a2c = Args2Config()
    config = a2c.get_config()
    args = a2c.parser.parse_args()
    if args.command == 'check':
        import_media(args.path, test=True,
                     config=config)
    if args.command == 'import':
        import_media(args.path, test=False,
                     config=config)
    elif args.command == 'serve':
        serve(config=config)
