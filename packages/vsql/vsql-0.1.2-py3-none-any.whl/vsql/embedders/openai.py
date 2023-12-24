from openai import OpenAI
import dotenv

client=OpenAI(api_key=dotenv.get('OPENAI_API_KEY'))
def embed(s):
    return client.embeddings.create( model="text-embedding-ada-002", input=s, encoding_format="float").data[0].embedding