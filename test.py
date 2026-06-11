from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma # uv add  chromadb langchain-chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# 使用本地 HuggingFace 嵌入模型（免费、无需 API key）
from langchain_huggingface import HuggingFaceEmbeddings

# ---------- 1. 加载文档 ----------
# 请确保 testFiles/sample.txt 存在且为 UTF-8 编码
documents = TextLoader("testFiles/sample.txt", encoding="utf-8").load()

# ---------- 2. 文档切分 ----------
splits = RecursiveCharacterTextSplitter(
    chunk_size=10,         # 每个文本块最大长度
    chunk_overlap=0,       # 相邻块之间的重叠长度
    separators=["\n\n", "\n", "。", "!", "?", "；", "，", " ", ""]  # 分隔符优先级
).split_documents(documents)

# ---------- 3. 创建本地嵌入模型 ----------
# model_name 可以是本地路径（如 "D:/ai_models/BAAI/bge-m3"）或 HuggingFace 模型名（如 "BAAI/bge-m3"）
# 若使用 HuggingFace 模型名且本地无缓存，首次运行会自动下载
embedding_model = HuggingFaceEmbeddings(
    model_name=r"D:\ai_models\BAAI\bge-m3",               # 可替换为本地路径 r"D:\ai_models\BAAI\bge-m3"
)

# ---------- 4. 创建向量数据库 ----------
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embedding_model,
    collection_name="rag_demo"
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})  # 检索最相似的3个片段

# ---------- 5. 创建对话模型（OpenAI GPT）----------
llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash"
)  # 需确保环境变量 OPENAI_API_KEY 已设置

# ---------- 6. 格式化检索到的文档 ----------
def format_docs(docs):
    """将检索到的文档列表拼接为一个上下文字符串"""
    print("\n\n---\n\n".join([
        f"[来源: {doc.metadata.get('source', '未知')}]\n{doc.page_content}"
        for doc in docs
    ]))
    print("-----------------------------------------------------------------")
    return "\n\n---\n\n".join([
        f"[来源: {doc.metadata.get('source', '未知')}]\n{doc.page_content}"
        for doc in docs
    ])

# ---------- 7. 构建 RAG 提示词模板 ----------
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有帮助的AI助手。请根据以下上下文回答问题。\n上下文：\n{context}"),
    ("human", "{question}")
])

# ---------- 8. 构建 RAG 链 ----------
# 流程：检索文档 → 格式化上下文 → 填充模板 → 大模型回答 → 解析字符串
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

# ---------- 9. 提问测试 ----------
response = rag_chain.invoke("我的名字叫")
print(response)