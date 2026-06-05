import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash"
)

# 1. 定义目标JSON结构
class Prime(BaseModel):
    prime: list[int] = Field(description="素数")
    count: list[int] = Field(description="小于该素数的素数个数")

# 2. 构造解析器
json_parser = JsonOutputParser(pydantic_object=Prime)
print(json_parser.get_format_instructions())
# 3. 将格式说明放入SystemMessage
# res = llm.invoke([
#     ("system", json_parser.get_format_instructions()),
#     ("user", "任意生成5个1000-100000之间的素数，并标出小于该素数的素数个数")
# ])
# print(res.content)
#
# # 4. 解析为Python字典
# parsed_res = json_parser.invoke(res)
# print(type(parsed_res))  # <class 'dict'>