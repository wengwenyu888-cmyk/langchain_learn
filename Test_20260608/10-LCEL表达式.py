from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from pydantic import BaseModel,Field

prompt = ChatPromptTemplate.from_template("请用{xxx}风格回答{question}")
llm = init_chat_model(model_provider='openai', model='deepseek-ai/DeepSeek-V4-Flash')

class Demo(BaseModel):
    title: str = Field(description='用户原始的问题')
    content: str = Field(description="大模型对于用于原始问题的回答")

llm_with_demo = llm.with_structured_output(schema=Demo)

# LCEL组合   - 像拼积木  链
chain = prompt | llm_with_demo # prompt.invoke() ---> llm.invoke()

res =chain.invoke({
    "xxx": '幽默',
    "question": '什么是爱?'
})
print(type(res))
print(res.title)
print(res.content)
# print(res['content'])

