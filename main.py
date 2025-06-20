from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from yt_dlp import YoutubeDL
import uvicorn

app = FastAPI()

# Разрешаем доступ с любых источников (в том числе с iPhone)
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
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "direct_url": info["url"],
                "title": info.get("title", "video")
            }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Запуск сервера вручную, если Render не найдёт порт
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
