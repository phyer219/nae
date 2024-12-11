from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
from .database_handle import NaeDatabase
from .default_config import NaeConfig
config = NaeConfig()
DATABASE_DIR = config.DATABASE_DIR
DATABASE_NAME = config.DATABASE_NAME
WEBUI_TEMPLATE_DIR = config.WEBUI_TEMPLATE_DIR

app = FastAPI()
templates = Jinja2Templates(directory=WEBUI_TEMPLATE_DIR)
# app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    nae_db = NaeDatabase(database_dir=DATABASE_DIR,
                         database_name=DATABASE_NAME)

    items = nae_db.getall()
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "songs": items, })


@app.get("/audio/{filename:path}")
def get_audio(filename: str):
    if filename.endswith(".mp3"):
        media_type = "audio/mpeg"
    elif filename.endswith(".flac"):
        media_type = "audio/flac"
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    return FileResponse(filename, media_type=media_type)


@app.get("/album/{album_id}", response_class=HTMLResponse)
def get_album(request: Request, album_id: int):
    nae_db = NaeDatabase(database_dir=DATABASE_DIR,
                         database_name=DATABASE_NAME)
    album = nae_db.db_select_tracks_from_albums(album_id)
    return templates.TemplateResponse("album.html", {"request": request,
                                                     "album": album, })
