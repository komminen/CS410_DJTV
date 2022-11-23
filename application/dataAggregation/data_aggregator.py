import re
import os
import json
import pickle
from imdb import Cinemagoer
from json_processor import json_zip, json_unzip

# create an instance of the Cinemagoer class
ia = Cinemagoer()

# Files Configuration
# From "Large Movie Review Dataset" (https://ai.stanford.edu/~amaas/data/sentiment/)
review_urls_filepaths = [
    'aclImdb/train/urls_neg.txt', 'aclImdb/train/urls_pos.txt', 'aclImdb/train/urls_unsup.txt',
    'aclImdb/test/urls_neg.txt', 'aclImdb/test/urls_pos.txt',
]
review_filepaths = [
    'aclImdb/train/neg', 'aclImdb/train/pos', 'aclImdb/train/unsup',
    'aclImdb/test/neg', 'aclImdb/test/pos',
]


def movie_metadata_extraction(movie_info, movie_id):
    try:
        movies_review[movie_id]["localized_title"] = movie_info.data["localized title"]
    except:
        movies_review[movie_id]["localized_title"] = ""

    try:
        movies_review[movie_id]["cast"] = [
            cast["name"] for cast in movie_info.data["cast"]
        ]
    except:
        movies_review[movie_id]["cast"] = []

    try:
        movie_reviews[movie_id]["genres"] = movie_info.data["genres"]
    except:
        movie_reviews[movie_id]["genres"] = []

    try:
        movies_review[movie_id]["runtimes"] = movie_info.data["runtimes"][0]
    except:
        movies_review[movie_id]["runtimes"] = ""

    try:
        movies_review[movie_id]["rating"] = movie_info.data["rating"]
    except:
        movies_review[movie_id]["rating"] = ""

    try:
        movies_review[movie_id]["year"] = movie_info.data["year"]
    except:
        movies_review[movie_id]["year"] = ""

    try:
        movies_review[movie_id]["producer"] = [
            cast["name"] for cast in movie_info.data["producer"]
        ]
    except:
        movies_review[movie_id]["producer"] = []

    try:
        movies_review[movie_id]["director"] = [
            cast["name"] for cast in movie_info.data["director"]
        ]
    except:
        movies_review[movie_id]["director"] = []

    try:
        movies_review[movie_id]["cover_url"] = movie_info.data["cover url"]
    except:
        movies_review[movie_id]["cover_url"] = ""

    try:
        movies_review[movie_id]["summary"] = movie_info.summary()
    except:
        movies_review[movie_id]["summary"] = ""


movies_review = {}
notfound_movies = {}

for review_filepath, url_filepath in tqdm(zip(review_filepaths, review_urls_filepaths)):

    # Read Review URLs
    with open(url_filepath) as f:
        review_urls = f.readlines()

    # Get the review file list
    review_files = os.listdir(review_filepath)

    for i in range(len(review_urls)):

        # Extract Movie ID
        movie_id = review_urls[i].split("/")[4].replace("tt", "")

        if movie_id not in movies_review:
            # Fetch Movie Metadata
            try:
                movie = ia.get_movie(movie_id)
            except:
                if movie_id not in notfound_movies:
                    notfound_movies[movie_id] = []
                notfound_movies[movie_id].append((review_filepath, i))
                continue

            movies_review[movie_id] = {}
            movie_metadata_extraction(movie_info, movie_id)
            movies_review[movie_id]["reviews"] = []

        # Find Corresponding Review filename
        r = re.compile(f"{i}_.*.txt")
        review_file = list(filter(r.match, review_files))

        assert len(review_file) == 1, "Wrong Filename Extraction"

        # Read Review File
        with open(f"{review_filepath}/{review_file[0]}", encoding="utf-8") as f:
            review = f.readlines()

        movies_review[movie_id]["reviews"].append(review)

    pickle.dump(movies_review, open("movies_review.p", "wb"))
    pickle.dump(notfound_movies, open("notfound_movies.p", "wb"))


# Dump dataset into zipped pickle
movies_review_json_zip = json_zip(movie_reviews)
pickle.dump(
    movies_review_json_zip, open(
        "../../data/movies_review_json_zip.p", "wb"
    )
)
