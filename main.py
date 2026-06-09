#模型下载
from modelscope import snapshot_download
model_dir = snapshot_download('BAAI/bge-base-zh-v1.5')
print(model_dir)