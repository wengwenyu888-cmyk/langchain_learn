
import os
import dotenv
dotenv.load_dotenv()

token = os.getenv("MINERU_TOKEN")

def mineru_upload_file_demo():
    import requests
    from pathlib import Path

    if not token:
        raise RuntimeError("环境变量 MINERU_TOKEN 未设置")

    # 1. 申请上传 URL
    url = "https://mineru.net/api/v4/file-urls/batch"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    # 本地文件路径列表（可扩展为多文件）
    file_paths = [
        r"test.pdf"
    ]

    files_info = []
    for i, p in enumerate(file_paths):
        p = Path(p)
        if not p.exists():
            raise FileNotFoundError(f"文件不存在: {p}")
        files_info.append({
            "name": p.name,
            "data_id": f"data_{i}",  # 自己给每个文件一个 data_id 标识
        })

    data = {
        "files":files_info,
        "model_version": "vlm",
    }

    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code != 200:
        print(f"申请上传 URL 失败，状态码：{resp.status_code}，响应内容：{resp.text}")
        return None

    result = resp.json()
    if result.get("code") != 0:
        print(f"申请上传 URL 失败，reason: {result.get('msg')}")
        return None

    print(result)

    batch_id = result["data"]["batch_id"]
    urls = result["data"]["file_urls"]
    print(f"申请上传 URL 成功，batch_id: {batch_id}")
    print("file_urls:", urls)

    # 2. 逐个上传文件到对应的临时 URL
    for i, upload_url in enumerate(urls):
        path = Path(file_paths[i])
        with path.open("rb") as f:
            res_upload = requests.put(upload_url, data=f)
        if res_upload.status_code == 200:
            print(f"{path.name} 上传成功")
        else:
            print(f"{path.name} 上传失败, 状态码: {res_upload.status_code}, 响应: {res_upload.text}")

    return batch_id, files_info


# mineru_upload_file_demo()
def mineru_check_result_demo(batch_id: str, max_retries: int = 30, interval: int = 3):
    """
    轮询 MinerU 批量解析结果，直到任务完成或超过重试次数。

    :param batch_id: 调用 /extract/task 时返回的 batch_id
    :param max_retries: 最大轮询次数
    :param interval: 每次轮询间隔秒数
    """
    import os
    import time
    import requests

    token = os.getenv("MINERU_TOKEN")
    if not token:
        raise RuntimeError("环境变量 MINERU_TOKEN 未设置")

    url = f"https://mineru.net/api/v4/extract-results/batch/{batch_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    for i in range(max_retries):
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"请求失败，状态码：{resp.status_code}，响应内容：{resp.text}")
            return None

        data = resp.json()
        # 结构示例：data["data"]["extract_result"] 是列表
        extract_list = data.get("data", {}).get("extract_result", [])
        if not extract_list:
            print("返回结果中没有 extract_result 字段：", data)
            return None

        item = extract_list[0]
        state = item.get("state")
        print(f"第 {i+1} 次查询，当前状态：{state}")

        if state == "done":
            full_zip_url = item.get("full_zip_url")
            print("任务已完成，结果 zip 下载地址：", full_zip_url)
            return full_zip_url
        elif state in ("failed", "error"):
            print("任务失败，返回信息：", item)
            return None

        # 还未完成，等待后重试
        time.sleep(interval)

    print(f"超过最大重试次数（{max_retries}），任务仍未完成，请稍后重试或在控制台查看状态。")
    return None


# 示例调用（替换为你自己的 batch_id）
mineru_check_result_demo("bb0f40ef-ac3d-420c-b6da-fdf127abdd40")