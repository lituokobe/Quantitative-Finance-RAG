from pymilvus import Collection
col = Collection("finance_chunks")
print(col.num_entities)