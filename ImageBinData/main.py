from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from PIL import Image
import io
from fastapi.responses import RedirectResponse

from core.crypto import genererCle, chiffrerMessage, dechiffrerMessage

app = FastAPI()

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

