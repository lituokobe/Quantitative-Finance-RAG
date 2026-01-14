import os
from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from sentence_transformers import SentenceTransformer
from config.paths import ENV_PATH, QWEN3_EMBEDDING_PATH

load_dotenv(ENV_PATH)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = os.getenv("OPENAI_URL")
ALI_API_KEY = os.getenv("ALI_API_KEY")
ALI_URL = os.getenv("ALI_URL")

agent_llm = ChatOpenAI(
    model = 'qwen-turbo',
    temperature = 0,
    api_key = ALI_API_KEY,
    base_url = ALI_URL,
)

evaluator_llm = ChatOpenAI(
    model = 'gpt-5-mini',
    temperature = 0,
    api_key = OPENAI_API_KEY,
    base_url = OPENAI_URL,
)

class CustomEmbedding(Embeddings):
    """
    Customize an Embedding class, integrated with LangChain
    """
    def __init__(self, model_name):
        self.embedding = SentenceTransformer(str(model_name))
    def embed_query(self, text : str) ->list[float]:
        return self.embed_documents([text])[0]
    def embed_documents(self, texts : list[str]) -> list[list[float]]:
        arr = self.embedding.encode(texts)
        return arr.tolist()

qwen3_embedding_model = CustomEmbedding(QWEN3_EMBEDDING_PATH)

openai_embedding = OpenAIEmbeddings()

if __name__ == "__main__":
    resp1 = evaluator_llm.invoke("How are you?")
    print(resp1.content)

    resp2 = agent_llm.invoke("How are you?")
    print(resp2.content)

    embed1 = qwen3_embedding_model.embed_query("good")
    print(embed1[:5])
    print(len(embed1))

    embed2 = openai_embedding.embed_query("good")
    print(embed2[5])
    print(len(embed2))