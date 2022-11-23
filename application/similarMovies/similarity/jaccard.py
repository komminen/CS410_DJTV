import numpy as np


class JaccardCalculator:

    def __init__(self, documents):
        self.documents = documents
        self.num_docs = len(documents)
        self.sim_matrix = np.zeros((self.num_docs, self.num_docs))

    def jaccardSimilarity(self, v1, v2):
        v1 = set(v1)
        v2 = set(v2)
        return float(len(v1 & v2)) / len(v1 | v2)

    def buildSimilarityMatrix(self):

        for d1 in range(self.num_docs):
            for d2 in range(d1, self.num_docs):
                doc_sim = self.jaccardSimilarity(
                    self.documents[d1], self.documents[d2]
                )
                # Symmetrics
                self.sim_matrix[d1][d2] = doc_sim
                self.sim_matrix[d2][d1] = doc_sim
