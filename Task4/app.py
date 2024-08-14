from flask import Flask, render_template, request
import pandas as pd
from create_movie_data import get_movie_data

app = Flask(__name__)

# Load the dataset from the create_movie_data.py
movies = get_movie_data()

# Function to get movie recommendations based on genre
def get_genre_recommendations(genre, num_recommendations=5):
    genre_movies = movies[movies['genre'].str.contains(genre, case=False)]
    recommendations = genre_movies.head(num_recommendations)
    return recommendations['title'].tolist()

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    if request.method == 'POST':
        genre = request.form['genre']
        recommendations = get_genre_recommendations(genre)
    return render_template('index.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
