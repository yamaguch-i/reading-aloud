# app.py
import os
import tempfile
import shutil
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.templating import Jinja2Templates

import asyncio
import edge_tts

app = FastAPI(title="On-Doku-san (Python TTS)")

# CORS（必要なら制限してください）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# 静的ファイル & テンプレート
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class TTSRequest(BaseModel):
    text: str = Field(min_length=1, description="読み上げ対象テキスト")
    voice: str = Field(default="ja-JP-NanamiNeural")
    rate: str = Field(default="+0%")  # 例: "-20%" ～ "+20%"
    filename: Optional[str] = None    # 任意：保存名

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/speak", response_class=FileResponse)
async def speak(payload: TTSRequest, background_tasks: BackgroundTasks):
    # 一時ディレクトリにMP3を生成 → レスポンス後に削除
    tmpdir = tempfile.mkdtemp(prefix="tts_")
    outpath = os.path.join(tmpdir, "speech.mp3")

    # 音声合成
    communicate = edge_tts.Communicate(
        payload.text,
        voice=payload.voice,
        rate=payload.rate
    )
    await communicate.save(outpath)

    # ダウンロード時のファイル名
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = payload.filename or f"speech_{ts}.mp3"

    # レスポンス送出後に後片付け
    background_tasks.add_task(shutil.rmtree, tmpdir, ignore_errors=True)

    return FileResponse(
        outpath,
        media_type="audio/mpeg",
        filename=fname,
        background=background_tasks,
    )

@app.get("/health")
def health():
    return {"status": "ok"}