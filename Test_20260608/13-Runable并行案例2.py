from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


llm = init_chat_model(model="deepseek-ai/DeepSeek-V4-Flash", model_provider="openai")

# 两个并行的赏析链
paragraph_1_chain = (
    PromptTemplate.from_template("对这首诗做赏析，分析含义：{poem}")
    | llm | StrOutputParser()
)
paragraph_2_chain = (
    PromptTemplate.from_template("对这首诗做赏析，分析意境：{poem}")
    | llm | StrOutputParser()
)

# 汇总链
summary_chain = (
    PromptTemplate.from_template(
        "第一种赏析：{paragraph_1}\n\n第二种赏析：{paragraph_2}\n\n请比较哪个更好，为什么"
    )
    | llm | StrOutputParser()
)

# 先并行，后汇总
full_chain = {
    "paragraph_1": paragraph_1_chain,
    "paragraph_2": paragraph_2_chain,
} | summary_chain

resp = full_chain.invoke({"poem": "菩提本无树，明镜亦非台，本来无一物，何处惹尘埃。"})
print(resp)