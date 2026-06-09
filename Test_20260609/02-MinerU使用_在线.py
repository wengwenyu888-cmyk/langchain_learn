# import requests
# import os
# import dotenv
# dotenv.load_dotenv()
#
# token = os.getenv("MINERU_TOKEN")
# url = "https://mineru.net/api/v4/extract/task"
# header = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer {token}"
# }
# data = {
#     "url": "https://cdn-mineru.openxlab.org.cn/demo/example.pdf",
#     "model_version": "vlm"
# }
#
# res = requests.post(url,headers=header,json=data)
# print(res.status_code)
# print(res.json())
# print(res.json()["data"])
# 文件上传成功
# cd5fd70c-647c-46d0-bd11-b059d6e3b8c2


# 有一个PDF（在线）   先上传

# 拿回分析后的结果

# 解析结果
import requests
import os
import dotenv
dotenv.load_dotenv()


token = os.getenv("MINERU_TOKEN")
task_id = "cd5fd70c-647c-46d0-bd11-b059d6e3b8c2"
url = f"https://mineru.net/api/v4/extract/task/{task_id}"
header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

res = requests.get(url, headers=header)
print(res.status_code)
print(res.json())
print(res.json()["data"])


