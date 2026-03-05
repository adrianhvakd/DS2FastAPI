from sqlalchemy import Column, Integer, String, Float
from database import Base
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(255))
    
class Producto(Base):
    __tablename__ = "producto"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Float)
    descripcion = Column(String, nullable=True)
    
class Categoria(Base):
    __tablename__ = 'categoria'
    
    id = Column(Integer, primary_key=True,index=True)
    nombre = Column(String,index=True)
