from langchain_huggingface import HuggingFaceEmbeddings

# 敲定使用哪款向量模型
embed_model = HuggingFaceEmbeddings(
    model_name=r'D:\ai_models\BAAI\bge-base-zh-v1___5'
)


# res = embed_model.embed_query('你好,世界')
# print(res)
# print(len(res))

res = embed_model.embed_documents(['你好世界','hello baby'])
print(len(res[0]))
print(res)