from langchain_core.runnables import RunnableLambda

def extract_domain(url):
    """从URL中提取域名"""
    return url.split('//')[-1].split('/')[0]

def add_protocol(domain):
    """添加协议前缀"""
    return f"http://{domain}"

# 包装成Runnable
domain_extractor = RunnableLambda(extract_domain)
protocol_adder = RunnableLambda(add_protocol)

# 在链中使用
url_processor = domain_extractor | protocol_adder
result = url_processor.invoke("https://www.example.com/path")
# 输出："http://www.example.com"
print(result)