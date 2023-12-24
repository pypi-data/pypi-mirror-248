from openai import OpenAI
client=OpenAI(api_key="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")
def embed(s):
    return client.embeddings.create( model="text-embedding-ada-002", input=s, encoding_format="float").data[0].embedding