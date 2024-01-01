<h1 align="center">VectorMass</h1>

<p align="center">
  <img width="200" src="./VectorMass/utils/vectormass_logo.png" alt="VectorMass vector database">
</p>


Vector databases are used to store vector embeddings for fast retrieval, similarity search, and other operations like crud operations. Simply, embedding is a numerical array that includes a huge number of features. So, using vector databases we can perform a lot of useful things on that numerical representation.

In traditional databases like <b>MySQL</b>, <b>PostgreSQL</b>, and <b>SQL Server</b> we are usually querying for rows in the database where the value matches our input query. In vector databases, we apply a similarity metric to find a vector that is the most similar to our query. There are a lot of dedicated vector databases out there such as <b>VectorMass</b>, <b>Pinecone</b>, <b>Qdrant</b>, <b>Chroma DB</b>, etc.

So, let’s learn how we can use <b>VectorMass</b> vector database…

```python
# install vectormass library
pip install VectorMass
```

```python
import VectorMass
import numpy as np

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-mpnet-base-v2')

# Create a VectorStore instance
vector_store = VectorMass.Client()

# Define your sentences
sentences = [
    "I eat mango",
    "mango is my favorite fruit",
    "mango, apple, oranges are fruits",
    "fruits are good for health",
]
ids = ['id1', 'id2', 'id3', 'id4']

# create a collection
collection = vector_store.create_or_get_collection("test_collection")

# add ids, documents and embeddings to the collection
collection.add(
    ids= ids,
    documents=sentences,
    embedding_model=model
)

# retrive data from the collection
# result = collection.get_all()
# print(result)

# querying
res = model.encode(['healthy foods', 'I eat mango'])
result = collection.query(query_embeddings=res)
print(result)
```

### Embeddings
Embeddings, in the context of machine learning and natural language processing (NLP), refer to numerical representations of words, sentences, or documents in a high-dimensional space. 
In <b>VectorMass</b> databse, use [<b>Sentence Transformer</b>](https://www.sbert.net/) embeddings as default embeddings. Upto now, it supports only embedding models which is in [<b>Sentence Transformer</b>](https://www.sbert.net/).

### License
[Apache 2.0](https://en.wikipedia.org/wiki/Apache_License)