from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from PIL import Image
import io
from fastapi.responses import RedirectResponse

from core.crypto import genererCle, chiffrerMessage, dechiffrerMessage
from core.encodaImage import cacherDonnees, extraireDonnees

app = FastAPI()

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.post("/cacher/")
async def cacherMessage(
    image: UploadFile = File(...),
    message: str = Form(...),
    motDePasse: str = Form(...)
):
    cle = genererCle()
    messageChiffre = chiffrerMessage(message, cle)
    imageOriginale = Image.open(image.file).convert("RGB")
    imageModifiee = cacherDonnees(imageOriginale, messageChiffre, motDePasse)
    tampon = io.BytesIO()
    imageModifiee.save(tampon, format="PNG")
    tampon.seek(0)
    return StreamingResponse(
        tampon,
        media_type="image/png",
        headers={"cle": cle.decode()}
    )

@app.post("/extraire/")
async def extraireMessage(
    image: UploadFile = File(...),
    cle: str = Form(...),
    motDePasse: str = Form(...)
):
    imageChargee = Image.open(image.file).convert("RGB")
    donneesCachees = extraireDonnees(imageChargee, motDePasse)
    message = dechiffrerMessage(donneesCachees, cle.encode())
    return {"message": message}
