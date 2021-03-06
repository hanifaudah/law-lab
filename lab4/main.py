from fastapi import Depends, FastAPI, HTTPException, UploadFile
from os import getenv
from dotenv import load_dotenv
# db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from db import crud, models, schemas
from db.database import SessionLocal, engine

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI(root_path=getenv("ROOT_PATH"))

# setup db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/mahasiswa/{npm}", response_model=schemas.Mahasiswa)
def read_mahasiswa_by_npm(npm:str, db: Session = Depends(get_db)):
    db_mahasiswa = crud.get_mahasiswa_by_npm(db, npm=npm)
    if not db_mahasiswa:
        raise HTTPException(status_code=400, detail="Mahasiswa not found")
    return db_mahasiswa

@app.post("/mahasiswa/", response_model=schemas.Mahasiswa)
def create_mahasiswa(mahasiswa: schemas.MahasiswaCreate, db: Session = Depends(get_db)):
    try:
        db_mahasiswa = crud.create_mahasiswa(db=db, mahasiswa=mahasiswa)
        return db_mahasiswa
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Mahasiswa already registered")

@app.put("/mahasiswa/{npm}", response_model=schemas.Mahasiswa)
def update_mahasiswa(mahasiswa: schemas.MahasiswaCreate, npm:str, db: Session = Depends(get_db)):
    db_mahasiswa = crud.get_mahasiswa_by_npm(db, npm=npm)
    if not db_mahasiswa:
        raise HTTPException(status_code=400, detail="Mahasiswa not found")
    return crud.update_mahasiswa(db=db, mahasiswa=mahasiswa, db_mahasiswa=db_mahasiswa)

@app.delete("/mahasiswa/{npm}")
def delete_mahasiswa(npm:str, db: Session = Depends(get_db)):
    db_mahasiswa = crud.get_mahasiswa_by_npm(db, npm=npm)
    if not db_mahasiswa:
        raise HTTPException(status_code=400, detail="Mahasiswa not found")
    crud.delete_mahasiswa(db=db, mahasiswa=db_mahasiswa)
    return { "message": "Mahasiswa deleted" }

@app.post("/files/")
async def upload_file(file: UploadFile, db: Session = Depends(get_db)):
    db_file = crud.create_file(db, file=file)
    return {"filename": db_file.file_name}
