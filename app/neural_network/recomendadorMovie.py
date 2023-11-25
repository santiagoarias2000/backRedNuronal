from fastapi import APIRouter, Depends, HTTPException
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.db import models
import pandas as pd
from tensorflow.keras.models import load_model
import numpy as np
import requests
from PIL import Image
from io import BytesIO
import imghdr

router = APIRouter(
    prefix="/neural_movies",
    tags=["Neural_Movies"]
)

# Cargar el modelo y los datos una sola vez cuando se inicia la aplicación
movies = pd.read_csv('https://hitwha.s3.amazonaws.com/movies2.csv')
model = load_model('app/neural_network/recomendadorMovies.h5')


# Función para obtener recomendaciones de películas
def get_movie_recommendations(movie_id):
    # Obtener géneros de la película seleccionada
    selected_movie_genres = movies.loc[movies['movieId'] == movie_id, 'genres'].values[0]

    # Filtrar películas no vistas por el usuario y con géneros similares
    movies_not_watched = movies[
        (movies['movieId'] != movie_id) & (movies['genres'].str.contains(selected_movie_genres))]

    # Seleccionar un subconjunto aleatorio de películas no vistas (por ejemplo, 10 películas)
    num_recommendations = 10
    random_movie_ids = np.random.choice(movies_not_watched['movieId'], num_recommendations, replace=False)

    # Verificar que los índices estén dentro del rango
    valid_movie_ids = random_movie_ids[random_movie_ids < len(movies)]

    # Obtener las predicciones solo para las películas no vistas seleccionadas aleatoriamente
    movie_input = np.array([movie_id] * len(valid_movie_ids))
    predictions = model.predict([np.zeros_like(movie_input), valid_movie_ids])

    # Crear un DataFrame con las predicciones y las películas correspondientes
    recommendations_df = pd.DataFrame({
        'movieId': valid_movie_ids,
        'predicted_rating': predictions.flatten()
    })

    # Ordenar las recomendaciones por puntuación predicha en orden descendente
    recommendations_df = recommendations_df.sort_values(by='predicted_rating', ascending=False)

    # Obtener información de las películas recomendadas
    recommended_movies_info = movies[movies['movieId'].isin(recommendations_df['movieId'])][
        ['movieId', 'title', 'genres', 'Poster']]

    # Fusionar la información de películas recomendadas con el DataFrame de recomendaciones
    recommendations_df = pd.merge(recommendations_df, recommended_movies_info, on='movieId')

    # Devolver información de las recomendaciones
    return recommendations_df[['movieId', 'title', 'genres', 'Poster', 'predicted_rating']]


# Ruta para obtener recomendaciones para una película específica
@router.get("/recommendations/{movie_id}")
def get_movie_recommendations_endpoint(movie_id: int):
    try:
        recommendations = get_movie_recommendations(movie_id)
    except:
        return {"message": "No te podemos recomendar peliculas"}
    return recommendations.to_dict(orient="records")


# Ruta para obtener detalles de una película específica
@router.get("/movie/{movie_id}")
def get_movie(movie_id: int):
    movie = movies.loc[movies['movieId'] == movie_id].to_dict(orient="records")
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"movie": movie[0]}
