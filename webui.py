import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .database_handle import NaeDatabase
from .default_config import NaeConfig


class WebUI:
    def __init__(self, config: NaeConfig):
        self.config = config
        self.app = FastAPI()
        self.templates = Jinja2Templates(
            directory=self.config.WEBUI_TEMPLATE_DIR)
        static_path = os.path.join(self.config.WEBUI_TEMPLATE_DIR, "static")
        self.app.mount("/static",
                       StaticFiles(directory=static_path),
                       name="static")
        self.db = NaeDatabase(config=self.config)
        self.register_routes()

    def register_routes(self):
        self.app.get("/", response_class=HTMLResponse)(self.index)
        self.app.get("/audio/{filename:path}")(self.get_audio)
        self.app.get("/album/{album_id}",
                     response_class=HTMLResponse)(self.get_album)

    def index(self, request: Request):
        tracks = self.db.get_all_tracks()
        return self.templates.TemplateResponse("index.html",
                                               {"request": request,
                                                "tracks": tracks})

    def get_audio(self, filename: str):
        if filename.endswith(".mp3"):
            media_type = "audio/mpeg"
        elif filename.endswith(".flac"):
            media_type = "audio/flac"
        else:
            raise HTTPException(status_code=400,
                                detail="Unsupported file type")
        return FileResponse(filename, media_type=media_type)

    def get_album(self, request: Request, album_id: int):
        album = self.db.db_select_tracks_from_albums(album_id)
        return self.templates.TemplateResponse("album.html",
                                               {"request": request,
                                                "album": album, })
