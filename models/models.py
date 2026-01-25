import os
from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_tavily import TavilySearch
from sentence_transformers import SentenceTransformer
from config.paths import ENV_PATH, QWEN3_EMBEDDING_PATH

# ======= Get the API keys ======
load_dotenv(ENV_PATH)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALI_API_KEY = os.getenv("ALI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# ======= LLM for the agent ======
agent_llm = ChatOpenAI(
    model = 'qwen-turbo',
    temperature = 0,
    api_key = ALI_API_KEY,
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# ======= LLM for the evaluator ======
evaluator_llm = ChatOpenAI(
    model = 'gpt-5-mini',
    temperature = 0,
    api_key = OPENAI_API_KEY,
    base_url = "https://api.openai.com/v1",
)

# ======= Embedding models ======
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

# ======= Wen search tool ======
web_search_tool = TavilySearch(tavily_api_key = TAVILY_API_KEY)

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