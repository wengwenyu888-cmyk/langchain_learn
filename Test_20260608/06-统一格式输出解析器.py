import os
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

# 1. 初始化LLM
llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash"
)

# 2. 定义Pydantic模型
class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

# 3. 使用with_structured_output，返回一个新的Runnable
structured_llm = llm.with_structured_output(schema=CalendarEvent)

# 4. 调用，直接返回Pydantic对象
result = structured_llm.invoke("Alice and Bob are going to a science fair on Friday.")
print(result)       # CalendarEvent(name='Science Fair', date='Friday', participants=['Alice', 'Bob'])
print(type(result)) # <class 'CalendarEvent'>