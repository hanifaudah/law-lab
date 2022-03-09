from sqlalchemy.orm import Session

from . import models, schemas


def get_mahasiswa(db: Session, id: int):
    return db.query(models.Mahasiswa).filter(models.Mahasiswa.id == id).first()


def get_mahasiswa_by_npm(db: Session, npm: str):
    return db.query(models.Mahasiswa).filter(models.Mahasiswa.npm == npm).first()


def get_mahasiswas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Mahasiswa).offset(skip).limit(limit).all()


def create_mahasiswa(db: Session, mahasiswa: schemas.MahasiswaCreate):
    db_mahasiswa = models.Mahasiswa(npm=mahasiswa.npm, nama=mahasiswa.nama, alamat=mahasiswa.alamat)
    db.add(db_mahasiswa)
    db.commit()
    db.refresh(db_mahasiswa)
    return db_mahasiswa

def update_mahasiswa(db: Session, mahasiswa: schemas.MahasiswaCreate, db_mahasiswa=models.Mahasiswa):
    db_mahasiswa.npm = mahasiswa.npm
    db_mahasiswa.nama = mahasiswa.nama
    db_mahasiswa.alamat = mahasiswa.alamat
    db.commit()
    db.refresh(db_mahasiswa)
    return db_mahasiswa

def delete_mahasiswa(db: Session, mahasiswa: schemas.MahasiswaCreate):
    db.delete(mahasiswa)
    db.commit()
