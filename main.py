from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn
from app.routes import movie
from app.neural_network import recomendadorMovie
from app.neural_network import topPelicula
from app.db.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware


def create_tables():
    Base.metadata.create_all(bind=engine)


create_tables()
print("creo")
'''


app = FastAPI()

class libros(BaseModel):
    titulo:str
    autor:str
    paginas:str
    editorial:Optional[str]

#Create rutes
@app.get("/")
def index():
    return {"message": "Hola python"}


@app.get("/libros/{id}")
def mostrar_libros(id:int):
    return {"data": id}


@app.post("/libros")
def insertar_libro(libro: libros):
    return {"message": f"libro {libro.titulo} insertado"}
'''
app = FastAPI()
origins =[
    'http://localhost',
    'http://localhost:8089',
    'http://localhost:8090',
    'https://movieflow-1e1cb.firebaseapp.com/'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(movie.router)
app.include_router(recomendadorMovie.router)
app.include_router(topPelicula.router)
movies = []

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
