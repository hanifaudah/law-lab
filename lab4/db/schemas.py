from typing import Optional

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