from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash"
)

# 同步调用
response = llm.invoke("你好")

# 流式调用 —— 逐token输出
for chunk in llm.stream("讲一个故事"):
    print(chunk.content, end="")

# 批量调用 —— 同时处理多个输入
responses = llm.batch(["你好", "再见", "谢谢"])

# 异步调用
import asyncio

res = asyncio.run(llm.ainvoke("你好"))