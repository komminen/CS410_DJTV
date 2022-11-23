import json
import pickle
from json_processor import json_zip, json_unzip

with open("../../data/movie_reviews_dataset.json") as data_file:
    movie_data_str = data_file.read()

movie_data = json.loads(movie_data_str)

# Separate two data files
# 1. Metadata File (movies_metadata.json)
# 2. Movies' Reviews File (movies_reviews.json)

movies_metadata = {}
movies_reviews = {}

for movie_id in movie_data:
    target_movie = movie_data[movie_id]

    movies_reviews[movie_id] = target_movie["reviews"]
    del target_movie["reviews"]
    movies_metadata[movie_id] = target_movie

# Store the data
with open("../../data/movies_metadata.json", "w") as outfile:
    json.dump(movies_metadata, outfile)


movies_review_json_zip = json_zip(movies_reviews)
pickle.dump(
    movies_review_json_zip, open(
        "../../data/movies_reviews_zip.p", "wb"
    )
)
