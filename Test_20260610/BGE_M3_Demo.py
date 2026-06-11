# uv add FlagEmbedding==1.3.5
# uv add transformers==4.44.2
from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel(model_name_or_path=r"D:\ai_models\BAAI\bge-m3")

text = "标量字段通常用来存储一些元数据，并可以在搜索时通过元数据进行过滤"

res = model.encode(
    [text],
    return_sparse=True,
    return_dense=True
)

print(res)

# print("=== 原始文本 ===")
# print(text)
# print("=" * 50)
#
# 1. 稀疏向量（关键词及其权重，原始 id 形式）
print("=== 稀疏向量（id → 权重）===")
lexical_weights = res["lexical_weights"][0]  # batch 中第一条
# 只看前若干个，避免太长
for i, (token_id, weight) in enumerate(list(lexical_weights.items())[:20]):
    print(f"[{i:02d}] id={token_id:<5}  weight={weight:.4f}")
print("...（仅展示前 20 个）")
print("=" * 50)
#
# # 2. 把稀疏向量的 id 转成可读 token
# print("=== 稀疏向量（token → 权重）===")
# sparse_tokens = model.convert_id_to_token(lexical_weights)
#
# for i, (token, weight) in enumerate(list(sparse_tokens.items())[:20]):
#     print(f"[{i:02d}] token='{token}'  weight={weight:.4f}")
#
# 3. 稠密向量（1024 维）
dense_vec = res["dense_vecs"][0]

print("=== 稠密向量信息 ===")
print(f"维度: {len(dense_vec)}")
print("前 10 维示例:")
# print(dense_vec[:10])
print([round(x, 4) for x in dense_vec])