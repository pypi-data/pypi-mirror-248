import faiss


class FaissIndexFlatIP:

    def __init__(self, dim):
        self.dim = dim
        self.index = faiss.IndexFlatIP(self.dim)
        self.ids = []
