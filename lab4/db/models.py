from sqlalchemy import Column, Integer, String, LargeBinary

from .database import Base

class Mahasiswa(Base):
    __tablename__ = "mahasiswa"

    id = Column(Integer, primary_key=True, index=True)
    npm = Column(String, unique=True, index=True)
    nama = Column(String)
    alamat = Column(String)

class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True, index=True)
    file = Column(LargeBinary)
    file_name = Column(String)
