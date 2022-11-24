import time

def queryMovies(query):

    output_dict = {
        "movie_name": query,
        "cover_url": "http://" + query + ".jpg"
    }

    return output_dict