import faiss
import numpy as np

class FlatFaissVDB:
    def __init__(self, ndim):
        self.index = faiss.IndexFlatL2(ndim)
        self.index = faiss.IndexIDMap(self.index)

    def search(self, query_vector, top_k):
        distances, indices = self.index.search(np.array([query_vector]).astype('float32'), top_k)
        # The indices array now contains the IDs directly
        return [int(i) for i in indices[0]], [float(d) for d in distances[0]]

    def add(self, id, embedding):
        self.index.add_with_ids(np.array([embedding]).astype('float32'), np.array([id]).astype('int64'))
