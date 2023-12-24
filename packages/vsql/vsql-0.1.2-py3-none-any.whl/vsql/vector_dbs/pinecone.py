# get pinecone_api_key from .env
import dotenv
dotenv.load_dotenv()
# import pinecone
import pinecone
pinecone.init(api_key=dotenv.get('PINECONE_API_KEY'), environment="us-west4-gcp") # init pinecone client

class PineconeVDB:
    def __init__(self):
        # TODO: this requires specifying an existing index w/ the correct dimensionality
        self.index = pinecone.Index("quickstart")

    def search(self, query_vector, top_k):
        search_results = self.index.query(query_vector, top_k=top_k)
        ids = [int(match['id']) for match in search_results.matches]
        similarities = [float(match['score']) for match in search_results.matches]
        return ids, similarities

    def add(self, id, embedding):
        self.index.upsert([{ 'id': str(id), 'values': embedding}])