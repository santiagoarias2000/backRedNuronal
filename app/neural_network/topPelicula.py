from keras.models import load_model
import pandas as pd
import numpy as np
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/top",
    tags=["Neural_Movies"]
)
# Cargar el modelo entrenado
loaded_model = load_model('app/neural_network/topMovies.h5')

# Cargar el DataFrame de películas
movies = pd.read_csv('https://hitwha.s3.amazonaws.com/movies2.csv')

# Crear un diccionario de índices para mapear el ID de las películas a un índice
movie_id_to_index = {movie_id: index for index, movie_id in enumerate(movies['movieId'].unique())}
movies['movieIndex'] = movies['movieId'].map(movie_id_to_index)

# Obtener el número de películas
num_movies = movies['movieIndex'].nunique()

# Generar predicciones para todas las películas
all_movies_input = np.arange(num_movies).reshape(-1, 1)
predictions = loaded_model.predict(all_movies_input)

# Agregar las predicciones como una nueva columna en el DataFrame de películas
movies['prediction'] = predictions

# Ordenar las películas por predicción en orden descendente para obtener las mejores recomendaciones
top_recommendations = movies.sort_values(by='prediction', ascending=False).head(10)

# Imprimir el top de películas recomendadas
print(top_recommendations[['title', 'prediction']])


@router.get("/top_recommendations")
async def get_top_recommendations():
    # Convertir el DataFrame a formato JSON y enviar como respuesta
    return top_recommendations.to_dict(orient="records")
