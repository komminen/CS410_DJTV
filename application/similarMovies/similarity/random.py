import random


class RandomCalculator:

    def __init__(self, movie_data, topK_movie):
        self.topK_movie = topK_movie
        self.movie_id_list = list(movie_data.keys())
        random.seed(9970)

    def generateSimilarMovies(self):
        similar_movies_result = {}
        for movie_id in self.movie_id_list:
            canidates = random.sample(self.movie_id_list, self.topK_movie + 1)
            similar_movies = [
                c for c in canidates if c != movie_id
            ][:self.topK_movie]
            similar_movies_result[movie_id] = similar_movies

        return similar_movies_result
