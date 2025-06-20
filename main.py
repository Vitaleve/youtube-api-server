from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from yt_dlp import YoutubeDL

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/download")
async def download_video(url: str = Query(..., description="YouTube URL")):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "format": "best",
            "cookiefile": "cookies.txt",  # <--- путь именно так
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return {
            "direct_url": info["url"],
            "title": info.get("title", "video")
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
