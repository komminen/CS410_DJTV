import gensim.downloader as api
import numpy as np


class GensimCalculator:

    def __init__(self, documents, pretrain_model="word2vec-google-news-300"):

        self.documents = documents
        self.num_docs = len(self.documents)
        self.sim_matrix = np.zeros((self.num_docs, self.num_docs))
        self.word_vectors = api.load(pretrain_model)
        self.vocab = set(self.word_vectors.index_to_key)
        self.documents_inscope_vocab = []
        self.preGenWordList()

    def preGenWordList(self):

        def genWordList(vocab):
            return [v for v in vocab if v in self.vocab]

        for doc in self.documents:
            self.documents_inscope_vocab.append(genWordList(doc))

    def n_Simiarity(self, v1, v2):

        if len(v1) == 0 or len(v2) == 0:
            return 0

        return self.word_vectors.n_similarity(v1, v2)

    def buildSimilarityMatrix(self):

        for d1 in range(self.num_docs):
            for d2 in range(d1, self.num_docs):
                doc_sim = self.n_Simiarity(
                    self.documents_inscope_vocab[d1],
                    self.documents_inscope_vocab[d2]
                )
                # Symmetrics
                self.sim_matrix[d1][d2] = doc_sim
                self.sim_matrix[d2][d1] = doc_sim
