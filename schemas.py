from pydantic import BaseModel,Field

# -------- Usuario --------

class UsuarioCreate(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6,max_length=72)


class UsuarioResponse(BaseModel):
    id: int
    username: str

    model_config = {"from_attributes": True}
# -------- Producto --------    
class ProductoBase(BaseModel):
    nombre: str
    precio: float
    descripcion: str | None = None   

class ProductoCreate(ProductoBase):
    pass
class ProductoUpdate(ProductoBase):
    nombre: str | None = Field(None,min_length=3,max_length=100)
    precio: float | None = Field(None,gt=0)
    descripcion: str | None = Field(None,max_length=100)
    
class ProductoResponse(ProductoBase):
    id: int    
    model_config = {
        "from_attributes": True
    }

class Categoria(BaseModel):
    nombre :str
    model_config = {
        "from_attributes": True
    }