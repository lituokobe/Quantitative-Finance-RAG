from pymilvus import MilvusClient

from config.paths import MILVUS_URI

client = MilvusClient(uri=MILVUS_URI)
schema = client.describe_collection("quantitative_finance_rag")
print(schema)
