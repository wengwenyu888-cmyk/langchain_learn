# JsonOutputParse json解析器 要求大模型按照json格式输出 本质 写提示词
# with_structured_output langchain提供统一调用原厂api
# ------------------
# StrOutputParse字符串
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 大模型对象
llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash"
)

prompt = ChatPromptTemplate.from_template(
    '你是一个资深的宠物起名大师,请为一只{color}颜色的{breed}起3个搞笑的名字')

chain = prompt | llm | StrOutputParser()

res = chain.invoke({'color': '橘色', 'breed': '狸花猫'})
print(res)
print(type(res))