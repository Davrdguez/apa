from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from converters.apa_converter import convert_to_apa
from uuid import uuid4
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_docx(
    file: UploadFile = File(...),
    titulo: str = Form(...),
    autor: str = Form(...),
    institucion: str = Form(...),
    carrera: str = Form(...),
    profesor: str = Form(...),
    ubicacion: str = Form(...),
    fecha: str = Form(...),
    referencias: str = Form("")
):
    os.makedirs("temp", exist_ok=True)

    input_path = os.path.join("temp", f"{uuid4()}_{file.filename}")
    output_path = input_path.replace(".docx", "_APA.docx")

    with open(input_path, "wb") as f:
        f.write(await file.read())

    convert_to_apa(
        input_path,
        output_path,
        titulo,
        autor,
        institucion,
        carrera,
        profesor,
        ubicacion,
        fecha,
        referencias
    )

    return FileResponse(
        output_path,
        filename="APA_convertido.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
