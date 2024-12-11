class NaeConfig:

    def __init__(self, **configs):
        self.DATABASE_DIR = './nae_library'
        self.DATABASE_NAME = 'nae_library.db'

        self.MEDIA_LIBRARY_PATH = './nae_library/media'
        self.KEEP_ORIGINAL_FILE = True

        self.WEBUI_TEMPLATE_DIR = "nae/templates"

        self.LOG_PATH = "./nae_library/nae.log"

        for key, value in configs.items():
            setattr(self, key, value)
