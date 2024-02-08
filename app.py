from flask import Flask, jsonify, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__)

df = pd.read_csv(r'C:\Users\USER\Desktop\movie_recommendation_system\data_set\movies.csv')
tfidf = TfidfVectorizer(stop_words='english')
df['overview'] = df['overview'].fillna('')
tfidf_matrix = tfidf.fit_transform(df['overview'])


@app.route('/home')
def home():
    return jsonify({'message': 'Welcome to the Home Page!'})


@app.route('/display_movies', methods=['GET'])
def get_movies():
    try:
        num_movies = int(request.args.get('num_movies', 7))
        selected_movies = df.head(num_movies)[['id', 'title']].to_dict(orient='records')
        return jsonify({"movies": selected_movies})
    except pd.errors.ParserError as e:
        print("Error parsing CSV file:", e)
        return jsonify({"error": "Error parsing CSV file"})


@app.route('/recommend_movies', methods=['POST'])
def recommend_movies():
    try:
        data = request.json
        selected_movie_title = data.get('title', '').lower()
        selected_movie_id = data.get('id')
        selected_movie_index = df[df['title'].str.lower() == selected_movie_title].index[0]
        selected_movie_vector = tfidf_matrix[selected_movie_index]
        cosine_similarities = linear_kernel(selected_movie_vector, tfidf_matrix).flatten()
        similar_movie_indices = cosine_similarities.argsort()[:-11:-1]
        similar_movie_indices = [idx for idx in similar_movie_indices if idx != selected_movie_index]
        recommended_movies = df.iloc[similar_movie_indices][['id', 'title']].to_dict(orient='records')
        return jsonify({"recommended_movies": recommended_movies})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred while recommending movies"})


@app.route('/search', methods=['GET'])
def search_movies():
    try:
        query = request.args.get('query', '')
        matching_rows = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
        selected_movies = matching_rows[['id', 'title']].to_dict(orient='records')
        return jsonify({"matching_movies": selected_movies})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred while searching movies"})


if __name__ == '__main__':
    app.run(debug=True)
