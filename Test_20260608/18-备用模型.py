import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser




# 2. 初始化主力模型（🚨 故意写错模型名，模拟主力大模型彻底瘫痪或欠费封号的绝境）
primary_llm = ChatOpenAI(
    model="xxxxxxxx",  # 绝对不存在的模型，调用必报错！
)

# 3. 初始化备用模型（准备一个便宜、稳定的模型接盘）
llm1 = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Flash"
)
llm2 = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V4-Pro"
)
# 4. 核心：为主力模型绑定回退（Fallback）方案
# 如果 primary_llm 报错，它会像抓手一样接住错误，立刻把输入转发给列表里的备用模型
llm_with_fallback = primary_llm.with_fallbacks([llm1, llm2])

# 5. 组装 LCEL 链（注意：把带回退能力的新对象放进链里）
fallback_chain = (ChatPromptTemplate.from_template("请用一句话解释什么是【{concept}】") |
                  llm_with_fallback |
                  StrOutputParser())

# 6. 执行调用
if __name__ == "__main__":
    print("🚀 正在发起请求（主力模型配置错误，观察系统是否会自动切到备用模型）...")

    try:
        # 即使主力模型 100% 会崩溃，整个链条依然能跑通！
        result = fallback_chain.invoke({"concept": "大模型回退机制"})

        print("\n✨ [调用成功] 最终大模型回复（注意，这其实是备用模型救场完成的）：")
        print(result)

    except Exception as e:
        print("\n❌ 完蛋，连备用模型也挂了：", e)
