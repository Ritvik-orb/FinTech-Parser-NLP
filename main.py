from fastapi import FastAPI, UploadFile, HTTPException
import os
import shutil
from ocr import extract_text
from ner import fintech_ner, classify_doc

app = FastAPI()


@app.post("/upload/")
async def upload(file: UploadFile):
    # ensure upload directory exists
    os.makedirs("files", exist_ok=True)
    filename = os.path.basename(file.filename)
    if not filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    path = f"files/{filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = extract_text(path)
    entities = fintech_ner(text)
    doc_type = classify_doc(text)

    return {"type": doc_type, "entities": entities, "text": text}
