import numpy as np


class MetricsEvaluator:

    def __init__(self, movie_data):
        self.movie_data = movie_data

    def evaluate_movie(self, target_movie, similar_movies):

        target_genres = set(self.movie_data[target_movie]["genres"])

        dcg_score = 0

        for i, movie_id in enumerate(similar_movies):
            relavent = 0
            for genre_pred in self.movie_data[movie_id]["genres"]:
                if genre_pred in target_genres:
                    relavent = 1
                    break

            if i > 0:
                dcg_score += relavent / np.log2(i + 1)
            else:
                dcg_score = relavent
        return dcg_score

    def evaluate(self, similarity_result):

        result = []
        for target_movie, sim_movies in similarity_result.items():
            result.append(self.evaluate_movie(target_movie, sim_movies))

        return result
