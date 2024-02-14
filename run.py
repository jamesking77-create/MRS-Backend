# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import os
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import linear_kernel
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import average_precision_score
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
# def create_test_data():
#     test_data = movies_df.sample(n=100, random_state=42)[['id', 'title', 'genres', 'overview']]
#     test_data['genres'] = test_data['genres'].apply(lambda x: [g['name'] for g in eval(x)])
#     return test_data.to_dict(orient='records')
#
#
# @app.route('/home')
# def home():
#     return jsonify({'message': 'Welcome to the Home Page!'})
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
# @app.route('/evaluate_recommendations', methods=['GET'])
# def evaluate_recommendations():
#     try:
#         # Step 1: Split the data into training and test sets
#         train_data, test_data = train_test_split(movies_df, test_size=0.2, random_state=42)
#
#         # Step 2: Generate recommendations for the test set
#         recommendations = {}
#         for index, row in test_data.iterrows():
#             selected_movie_title = row['title'].lower()
#             selected_movie_index = movies_df[movies_df['title'].str.lower() == selected_movie_title].index[0]
#             selected_movie_vector = tfidf_matrix[selected_movie_index]
#             cosine_similarities = linear_kernel(selected_movie_vector, tfidf_matrix).flatten()
#             similar_movie_indices = cosine_similarities.argsort()[:-11:-1]
#             similar_movie_indices = [idx for idx in similar_movie_indices if idx != selected_movie_index]
#             recommended_movies = movies_df.iloc[similar_movie_indices][['id', 'title']].to_dict(orient='records')
#             recommendations[row['id']] = [movie['id'] for movie in recommended_movies]
#
#         # Step 3: Evaluate the recommendations using Mean Average Precision (MAP)
#         average_precision = 0
#         num_evaluated = 0
#
#         for movie_id, recs in recommendations.items():
#             true_labels = [1 if movie_id in test_data[test_data['id'] == rec]['id'].values else 0 for rec in recs]
#             if sum(true_labels) > 0:
#                 average_precision += average_precision_score(true_labels, range(1, len(true_labels) + 1))
#                 num_evaluated += 1
#
#         mean_average_precision = average_precision / num_evaluated if num_evaluated > 0 else 0
#
#         return jsonify({"mean_average_precision": mean_average_precision})
#
#     except Exception as e:
#         print("Error:", e)
#         return jsonify({"error": "An error occurred while evaluating recommendations"})
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
