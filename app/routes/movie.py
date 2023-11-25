from fastapi import APIRouter, Depends, requests
from app.shemas import Movies, MoviesId
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.db import models

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)

movies = []


@router.get("/view_movies")
def get_movies(db: Session = Depends(get_db)):
    data = db.query(models.Movies).all()
    movies_list = [{"id": movie.id, "name": movie.name, "genre": movie.gender, "image": movie.image} for movie in data]
    return movies_list


@router.get("/view_movies_pag")
def get_movies(page: int = 1, page_size: int = 30, db: Session = Depends(get_db)):
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    data = db.query(models.Movies).slice(start_index, end_index).all()
    movies_list = []

    for movie in data:
        if movie.image:
            movies_list.append({"id": movie.id, "name": movie.name, "genre": movie.gender, "image": movie.image})
        else:
            print(f"Pelicula {movie.id} no cuenta con imagen")

    return movies_list


@router.post('/create_movies')
def ruta2(movie: Movies):
    movie = movie.dict()
    movies.append(movie)
    print(movie)
    return {"Response": "movie create successful"}


@router.post("/movie/{movie_id}")
def get_movie(movie_id: int):
    for movie in movies:
        print(movie, type(movie))
        if movie["id"] == movie_id:
            return {"movie": movie}
    return {"respuesta": "user not found"}


@router.post("/movies2")
def get_user_2(movie_id: MoviesId):
    for movie in movies:
        print(movie, type(movie))
        if movie["id"] == movie_id.id:
            return {"movie": movie}
    return {"respuesta": "user not found"}
