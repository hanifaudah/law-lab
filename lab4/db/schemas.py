from pydantic import BaseModel

class MahasiswaBase(BaseModel):
    npm: str
    nama: str
    alamat: str


class MahasiswaCreate(MahasiswaBase):
    pass


class Mahasiswa(MahasiswaBase):
    id: int

    class Config:
        orm_mode = True

class File(BaseModel):
    id: int
    file: bytes
    file_name: str
    
    class Config:
        orm_mode = True
