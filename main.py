from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel
from typing import List, Annotated
from fastapi.middleware.cors import CORSMiddleware
import models 
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import schemas
from auth import (
    get_db, hash_password, verify_password,
    create_token, get_current_user
)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
models.Base.metadata.create_all(bind=engine)
        
db_dependency = Annotated[Session,Depends(get_db)]

@app.post("/", response_model=schemas.UsuarioResponse)
def register(user: schemas.UsuarioCreate, db : db_dependency):
    existing = db.query(models.Usuario).filter(
        models.Usuario.username == user.username
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    
    new_user = models.Usuario(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# -------- LOGIN --------

@app.post("/login")
def login(user: schemas.UsuarioCreate, db : db_dependency):
    db_user = db.query(models.Usuario).filter(
        models.Usuario.username == user.username
    ).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    token = create_token({"sub": db_user.username})

    return {"access_token": token, "token_type": "bearer"}


# -------- CRUD PRODUCTOS --------
@app.get("/producto/",response_model=list[schemas.ProductoResponse])
def products( db : db_dependency,user: models.Usuario = Depends(get_current_user)):
    return db.query(models.Producto).filter(models.Producto.precio>0).all()
@app.post("/producto/",response_model=schemas.ProductoResponse)
def products( 
             producto: schemas.ProductoCreate, 
             db : db_dependency,
             user: models.Usuario = Depends(get_current_user)):
    nuevo_producto = models.Producto(
        **producto.model_dump()
    )
    db.add(nuevo_producto)     # agrega a la sesión
    db.commit()                # guarda en la BD
    db.refresh(nuevo_producto) 
    return nuevo_producto
@app.put("/producto/{id}",response_model=schemas.ProductoResponse)
def products(id:int, producto:schemas.ProductoUpdate, db : db_dependency):
    prod = db.query(models.Producto).filter(models.Producto.id==id).first()
    if not prod:
        raise HTTPException(status_code=404,detail="Producto no encontrado")
    for key, value in producto.model_dump(exclude_unset=True).items():
        setattr(prod,key,value)
    db.commit()
    db.refresh(prod)
    return prod
@app.delete("/producto/{id}")
def products(id:int, db : db_dependency):
    producto = db.query(models.Producto).filter(models.Producto.id==id).first()
    if not producto:
        raise HTTPException(status_code=404,detail='producto no encontrado')
    db.delete(producto)
    db.commit()
    return {'message':'producto eliminado'}