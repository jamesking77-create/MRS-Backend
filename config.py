# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import os
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import linear_kernel
#
# app = Flask(__name__)
# CORS(app, origins='*')
#
# current_dir = os.path.dirname(os.path.abspath(__file__))
#
# movies_csv_path = os.path.join(current_dir, 'data_set', 'movies.csv')
# credits_csv_path = os.path.join(current_dir, 'data_set', 'credits.csv')
#
# movies_df = pd.read_csv(movies_csv_path)
# credits_df = pd.read_csv(credits_csv_path)
#
# tfidf = TfidfVectorizer(stop_words='english')
# movies_df['overview'] = movies_df['overview'].fillna('')
# tfidf_matrix = tfidf.fit_transform(movies_df['overview'])
#
#
# @app.route('/home')
# def home():
#     return jsonify({'message': 'Welcome to the Home Page oooooo!'})
#
#
# @app.route('/display_movies', methods=['GET'])
# def get_movies():
#     try:
#         num_movies = int(request.args.get('num_movies', 7))
#         selected_movies = movies_df.head(num_movies)[['id', 'title']].to_dict(orient='records')
#         return jsonify({"movies": selected_movies})
#     except pd.errors.ParserError as e:
#         print("Error parsing CSV file:", e)
#         return jsonify({"error": "Error parsing CSV file"})
#
#
# @app.route('/recommend_movies', methods=['POST'])
# def recommend_movies():
#     try:
#         data = request.json
#         selected_movie_title = data.get('title', '').lower()
#         selected_movie_id = data.get('id')
#         selected_movie_index = movies_df[movies_df['title'].str.lower() == selected_movie_title].index[0]
#         selected_movie_vector = tfidf_matrix[selected_movie_index]
#         cosine_similarities = linear_kernel(selected_movie_vector, tfidf_matrix).flatten()
#         similar_movie_indices = cosine_similarities.argsort()[:-11:-1]
#         similar_movie_indices = [idx for idx in similar_movie_indices if idx != selected_movie_index]
#         recommended_movies = movies_df.iloc[similar_movie_indices][['id', 'title']].to_dict(orient='records')
#         return jsonify({"recommended_movies": recommended_movies})
#     except Exception as e:
#         print("Error:", e)
#         return jsonify({"error": "An error occurred while recommending movies"})
#
#
# @app.route('/search_movies', methods=['GET'])
# def search_movies():
#     try:
#         query = request.args.get('query', '')
#         matching_movies = movies_df[
#             movies_df['title'].str.contains(query, case=False, na=False) |
#             movies_df['keywords'].apply(lambda x: query in str(x).lower()) |
#             movies_df['tagline'].str.contains(query, case=False, na=False) |
#             movies_df['production_companies'].apply(
#                 lambda x: any(query.lower() in company['name'].lower() for company in eval(x)))
#             ]
#         selected_movies = matching_movies[['id', 'title']].to_dict(orient='records')
#         return jsonify({"matching_movies": selected_movies})
#     except Exception as e:
#         print("Error:", e)
#         return jsonify({"error": "An error occurred while searching movies"})
#
#
# @app.route('/search_credits', methods=['GET'])
# def search_credits():
#     try:
#         query = request.args.get('query', '').lower()
#
#         matching_credits = credits_df[
#             credits_df['cast'].apply(lambda x: any(
#                 query in actor['name'].lower() or query in actor['character'].lower() for actor in eval(x))) |
#             credits_df['crew'].apply(lambda x: any(query.lower() in member['name'].lower() for member in eval(x)))
#             ]
#
#         selected_credits = matching_credits[['movie_id', 'title']].to_dict(orient='records')
#
#         return jsonify({"matching_credits": selected_credits})
#     except Exception as e:
#         print("Error:", e)
#         return jsonify({"error": "An error occurred while searching credits"})
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
