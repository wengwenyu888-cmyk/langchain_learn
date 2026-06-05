from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field, field_validator
from langchain_openai import ChatOpenAI

# 1. 定义数据模型（保持不变）
class MovieReview(BaseModel):
    """电影评论结构"""
    title: str = Field(description="电影标题")
    rating: int = Field(description="评分，1-10分", ge=1, le=10)
    summary: str = Field(description="剧情简介")
    recommended: bool = Field(description="是否推荐")



# 2. 初始化大模型
llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash"
)

# 3. 让大模型与 Pydantic 结构强绑定
# with_structured_output 会在底层自动处理 schema 注入，无需我们在 Prompt 中手动配置
structured_llm = llm.with_structured_output(schema=MovieReview)

# 4. 干净、纯粹的 Prompt 模板（再也没有大括号报错的隐患）
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的电影评论家。请根据用户提供的电影，返回规范的结构化评论数据。"),
    ("human", "评价电影《{movie_name}》")
])

# 5. 组合 LCEL 链：Prompt 直接对接强绑定的模型（不再需要 parser 组件）
chain = prompt | structured_llm

# 6. 调用并传入变量
result = chain.invoke({"movie_name": "盗梦空间"})

# 7. 打印结果（result 直接就是一个 MovieReview 的 Pydantic 对象）
print(f"电影: {result.title}")
print(f"评分: {result.rating}/10")
print(f"简介: {result.summary}")
print(f"推荐: {'是' if result.recommended else '否'}")