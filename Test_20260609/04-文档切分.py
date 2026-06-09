from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredWordDocumentLoader


# 文档加载
docs = UnstructuredWordDocumentLoader(
    file_path=r"D:\BaiduSyncdisk\11-LangChain\课件及资料\RAG测试文件\sample.docx",
    mode='single'
).load()


# 切分为文本块
chunks = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "。", "！", "？", "……", "，", ""],
    chunk_size=400,# 每个块的长度,
    chunk_overlap=50, # 相邻块重叠长度
    length_function=len, # 长度计算函数
).split_documents(docs)

print(len(chunks))
print("-------------------------------------")
for i, chunk in enumerate(chunks[:5]):# 只看前5个块
    print(f"{chunk.page_content} \n {chunk.metadata}")
    print("888888888888888888888888888888888888888888888888")
