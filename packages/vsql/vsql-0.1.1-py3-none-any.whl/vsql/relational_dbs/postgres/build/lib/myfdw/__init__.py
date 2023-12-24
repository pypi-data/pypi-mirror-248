from multicorn import ForeignDataWrapper
# you can't print from python to stdout
# instead you'll have to use the utils module for logging and error reporting (this seems like imperfect design)

from openai import OpenAI
client=OpenAI(api_key="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")
def embed(s):
    return client.embeddings.create( model="text-embedding-ada-002", input=s, encoding_format="float").data[0].embedding
import pinecone
pinecone.init(api_key="dc18c259-4824-4f7b-b855-b8f78fef3cb0", environment="us-west4-gcp") # init pinecone client
index = pinecone.Index("quickstart")
def search(query_vector, top_k):
    search_results = index.query(query_vector, top_k=top_k)
    ids = [int(match['id']) for match in search_results.matches]
    similarities = [float(match['score']) for match in search_results.matches]
    return ids, similarities


class ConstantForeignDataWrapper(ForeignDataWrapper):

    def __init__(self, options, columns):
        # options (minus the name of the module) is just passed along from multicorn
        # columns is a dictionary mapping column names to datatypes
        self.columns = [{'id': 'integer', 'query': 'text', 'similarity': 'numeric'}]
        super(ConstantForeignDataWrapper, self).__init__(options, self.columns)
        # TODO: allow metadata
        # TODO: allow the indexed column to be named.
        # TODO: choose the appropriate index based on the options

    def execute(self, quals, columns, sortkeys=None):
        # returns a generator of lines, each line represented as a dictionary from col names to datatypes
        # quals restrict the result set and have three attributes: col_name, operator, value
        # unfortunately multicorn doesn't provide a way to tell postgres that a qual has already been applied.
        # this means that pg will recheck all the quals.
        # for me this means that we will have to return query=query because they might try sel * from vdb where ...
        # assert that we have 
        assert any([sk.attname=='similarity' and not sk.is_reversed for sk in sortkeys]), "vector index requires ORDER BY similarity"
        query_quals = [qual for qual in quals if qual.field_name=='query' and qual.operator=='=']
        assert query_quals, "vector index must be queried with the filter query=XXX"
        query = query_quals[0].value
        # embed
        query_vector = embed(query)
        # search the pinecone vindex
        best_ids, similarities = search(query_vector, top_k=10)
        # return a generator. Technically we don't get any performance benefit from a generator here
        # but we could make things better later by having a 100/10k access pattern on the vdb
        for id, similarity in zip(best_ids, similarities):
            line = {'id': id, 'query': query, 'similarity': similarity}
            yield line

    def can_sort(self, sortkeys):
        # takes a list of columns on which to sort [('c1','asc'), ('c2','desc'), ...]
        # returns a list of columns for which the fdw can enforce the sorting
        # by telling them we can sort by similarity, the query optimizer will choose us first!
        return sortkeys  # indicate we can handle all sorting