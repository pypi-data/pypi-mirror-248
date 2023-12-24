import pinecone

class PineconeVDB:
    def __init__(self):
        pinecone.init(api_key="dc18c259-4824-4f7b-b855-b8f78fef3cb0", environment="us-west4-gcp") # init pinecone client
        # TODO: this requires specifying an existing index w/ the correct dimensionality
        self.index = pinecone.Index("quickstart")

    def search(self, query_vector, top_k):
        search_results = self.index.query(query_vector, top_k=top_k)
        ids = [int(match['id']) for match in search_results.matches]
        similarities = [float(match['score']) for match in search_results.matches]
        return ids, similarities

    def add(self, id, embedding):
        self.index.upsert([{ 'id': str(id), 'values': embedding}])