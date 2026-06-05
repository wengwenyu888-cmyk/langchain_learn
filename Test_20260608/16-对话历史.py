from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

store = {}


# 用于存取数据的 函数
def get_session_history(session_id: str):
    if session_id not in store:
        # session_id 开辟
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


# 提示词模版
prompt = ChatPromptTemplate.from_messages([
    ('system', '你是一个AI助手'),
    MessagesPlaceholder(variable_name='history'),
    ('human', '{input}')
])
llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash"
)  # 初始化大语言模型
# 最基础链 输入数据  填入模板  发给模型
chain = prompt | llm
# 包装上记忆组件
chain_with_history = RunnableWithMessageHistory(
    chain,  # 把链交给 记忆管家
    get_session_history,
    input_messages_key='input',
    history_messages_key='history',
)

# 多轮对话测试
res1 = chain_with_history.invoke(
    {'input': '我叫牛依豪'},
    config={'configurable': {'session_id': 'niuyihao'}}  # 告诉管家 我是谁
)
print(res1.content)
print("-----------------------------")
res2 = chain_with_history.invoke(
    {'input': '我叫什么'},
    config={'configurable': {'session_id': 'niuyihao'}}  # 告诉管家 我是谁
)
print(res2.content)
