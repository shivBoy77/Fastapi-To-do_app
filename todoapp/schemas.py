from typing import List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass

# TOD SHIT ************************


class JobCreate(BaseModel):
    title: str
    description: str


class JobBase(BaseModel):
    title: str
    description: str
    salary: int


class JobCreateo(JobBase):
    symbol: str
    # title: str
    # desc: str


class Job(JobBase):
    id: int
    done: bool = False

    class config:
        orm_mode = True

# ***************************************


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
