from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select
from pydantic import BaseModel
from typing import Optional
import bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

PEPPER = os.getenv("PEPPER")

app = FastAPI()

base_datos = create_engine("sqlite:///database.db")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    hashed_password: str

class LoginData(BaseModel):
    username: str
    password: str

SQLModel.metadata.create_all(base_datos)

@app.post("/register")
def register(data: LoginData):
    with Session(base_datos) as session:
        user = session.exec(
            select(User).where(User.username == data.username)
        ).first()
        if user:
            raise HTTPException(
                status_code=400,
                detail="Usuario ya existe"
            )
        password = data.password + PEPPER
        hashed = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()
        new_user = User(
            username=data.username,
            hashed_password=hashed
        )
        session.add(new_user)
        session.commit()
        return {
            "message": "Usuario registrado"
        }

@app.post("/login")
def login(data: LoginData):
    with Session(base_datos) as session:
        user = session.exec(
            select(User).where(User.username == data.username)
        ).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )
        password = data.password + PEPPER
        valid = bcrypt.checkpw(
            password.encode(),
            user.hashed_password.encode()
        )
        if not valid:
            raise HTTPException(
                status_code=401,
                detail="Contraseña incorrecta"
            )
        return {
            "message": "Login correcto"
        }