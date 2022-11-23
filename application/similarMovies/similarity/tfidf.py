import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TFIDFCalculator:

    def __init__(self, documents):
        self.documents = documents
        self.num_docs = len(self.documents)
        self.sim_matrix = None
        self.vectorizer = TfidfVectorizer()

        # Build Vocab
        self.embedding = self.vectorizer.fit_transform(self.documents)

    def buildSimilarityMatrix(self):

        self.sim_matrix = cosine_similarity(self.embedding, self.embedding)
