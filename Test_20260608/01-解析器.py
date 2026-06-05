from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash"
)
class Joke(BaseModel):
    title: str = Field(description='笑话的标题,简洁有趣')
    content: str = Field(description='笑话的正文内容,幽默诙谐')
    theme: str = Field(description='笑话的主题,比如 日常、职场、动物')

# 以json格式输出  langchain json解释器 JsonOutputParser()
jsp = JsonOutputParser(pydantic_object=Joke)
res = llm.invoke([
    ('system', jsp.get_format_instructions()),
    ('human', "请你给我讲一个笑话,幽默诙谐")]
)
print(res.content)
print(type(res.content))
pe = jsp.invoke(res.content) # 转回来 python的对象
print("---------------------")
print(type(pe))
print(pe['title'])
print(pe['content'])
print(pe['theme'])



