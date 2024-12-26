import os
import pkg_resources


class NaeConfig:

    def __init__(self, **configs):
        self.BASE_DIR = './nae_library'
        self.DATABASE_DIR = self.BASE_DIR

        self.DATABASE_NAME = 'nae_library.db'

        self.MEDIA_LIBRARY_PATH = os.path.join(self.BASE_DIR, 'media')
        self.KEEP_ORIGINAL_FILE = True

        self.WEBUI_TEMPLATE_DIR = pkg_resources.resource_filename(
            'nae', 'templates'
        )

        self.LOG_PATH = os.path.join(self.BASE_DIR, 'nae.log')

        self.PORT = 8000

        for key, value in configs.items():
            setattr(self, key, value)
