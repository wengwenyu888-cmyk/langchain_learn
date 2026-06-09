import os
from pathlib import Path

from langchain_community.document_loaders import UnstructuredMarkdownLoader, UnstructuredWordDocumentLoader


def md_load_demo(file_path: str):
    loader = UnstructuredMarkdownLoader(
        file_path,  # 路径
        encoding="utf-8",  # 编码格式
        mode="elements",  # 按照标题、段落、列表等元素进行文档的切分
    )
    # 文档加载 list[Document]:
    docs = loader.load()

    for i, doc in enumerate(docs):
        print(f"{i}. {doc.page_content} \n {doc.metadata}")


def word_load_demo(file_path: str, start: int = 0, end: int = 20):
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f'文件路径不存在:{file_path.resolve()}')

    loader = UnstructuredWordDocumentLoader(
        file_path=str(file_path),
        mode='elements',  # 按行切割
    )

    docs = loader.load()
    print(len(docs))

    # page_content 数据
    # 元数据 ：描述信息  来源 id 长度...

    for i, doc in enumerate(docs[start:end]):
        print(f"{i}. {doc.page_content} \n {doc.metadata}")



if __name__ == "__main__":
    word_load_demo(r"D:\BaiduSyncdisk\11-LangChain\课件及资料\RAG测试文件\sample.docx")
    # md_load_demo(r"D:\BaiduSyncdisk\11-LangChain\课件及资料\RAG测试文件\sample.md")
