from typing import List

from fastapi import Depends, FastAPI, HTTPException

# db
from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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
    db_mahasiswa = crud.get_mahasiswa_by_npm(db, npm=mahasiswa.npm)
    if db_mahasiswa:
        raise HTTPException(status_code=400, detail="Mahasiswa already registered")
    return crud.create_mahasiswa(db=db, mahasiswa=mahasiswa)

@app.put("/mahasiswa/{npm}", response_model=schemas.Mahasiswa)
def update_mahasiswa(mahasiswa: schemas.MahasiswaCreate, npm:str, db: Session = Depends(get_db)):
    db_mahasiswa = crud.get_mahasiswa_by_npm(db, npm=npm)
    if not db_mahasiswa:
        raise HTTPException(status_code=400, detail="Mahasiswa not found")
    return crud.update_mahasiswa(db=db, mahasiswa=mahasiswa, db_mahasiswa=db_mahasiswa)

@app.delete("/mahasiswa/")
def delete_mahasiswa(npm:str, db: Session = Depends(get_db)):
    db_mahasiswa = crud.get_mahasiswa_by_npm(db, npm=npm)
    if not db_mahasiswa:
        raise HTTPException(status_code=400, detail="Mahasiswa not found")
    crud.delete_mahasiswa(db=db, mahasiswa=db_mahasiswa)
    return { "message": "Mahasiswa deleted" }