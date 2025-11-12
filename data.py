from huggingface_hub import hf_hub_download
import os
from tqdm import tqdm

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
# 下载 zip 文件（自动缓存）
print("📥 正在从 HuggingFace 下载数据集...")
zip_path = hf_hub_download(
    repo_id="p1k0/practice_ds_500",
    filename="practice_ds_500.zip",
    repo_type="model",
    local_dir= "/mnt/workspace/xintong/dataset/"
)
target_dir = "/mnt/workspace/xintong/dataset/"

os.system(f'unzip -o {zip_path} -d {target_dir}')