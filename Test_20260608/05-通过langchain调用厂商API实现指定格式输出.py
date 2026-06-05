from langchain_openai import ChatOpenAI
from pydantic import BaseModel,Field

llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash",
    temperature=0.0
)

class Demo(BaseModel):
    name: str = Field(description="收件人姓名")
    phone: str = Field(description='收件手机号')
    address : str = Field(description='收件人地址')

# langchain统一写法
# sp 是输出解析器
sp = llm.with_structured_output(schema=Demo)

# 模拟
raw_text = "给张三寄个快递，电话是13812345678。地址在上海市浦东新区世纪大道1号金茂大厦5楼。"

res = sp.invoke(raw_text)
print(res)