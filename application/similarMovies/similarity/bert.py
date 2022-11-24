import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class BERTCalculator:

    def __init__(self, documents, model_name="bert-base-nli-mean-tokens"):
        self.documents = documents
        self.num_docs = len(self.documents)
        self.sim_matrix = None
        self.model = SentenceTransformer(model_name)

        # Build Vocab
        self.embedding = self.model.encode(self.documents)

    def buildSimilarityMatrix(self):

        self.sim_matrix = cosine_similarity(self.embedding, self.embedding)
