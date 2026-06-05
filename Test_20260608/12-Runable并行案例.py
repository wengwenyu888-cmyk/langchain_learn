from langchain_core.runnables import RunnableSequence, RunnableParallel, RunnableLambda

# 创建顺序任务 RunnableSequence
# 创建一个并行任务RunnableParallel
# p_chain = RunnableParallel({
#     'a': RunnableLambda(lambda x: len(x)),  #
#     'b': RunnableLambda(lambda x: x.upper()),
#     'c': RunnableLambda(lambda x: len(x.split())),
#     'd': RunnableLambda(lambda x: x[::-1]),
# })
# res = p_chain.invoke("hello wolrd LangChain")
# print(res)
# chain = {
#     "length": RunnableLambda(lambda x: len(x)),
#     "uppercase": RunnableLambda(lambda x: x.upper()),
#     "reversed": RunnableLambda(lambda x: x[::-1]),
#     "word_count": RunnableLambda(lambda x: len(x.split()))
# }