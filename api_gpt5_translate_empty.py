# pip install openai==1.35.10
import datetime
import json
import openai
import time
import base64
import tqdm
from pathlib import Path
from io import BytesIO
import os
import argparse
import sys
import requests

with open('/mnt/workspace/xintong/api_key.txt', 'r') as f:
    lines = f.readlines()

API_KEY = lines[0].strip()
BASE_URL = lines[1].strip()

openai.api_key = API_KEY
openai.base_url = BASE_URL
lang_map = {
    "en": "English",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    'de': "German",
    'fr': "French",
    'it': "Italian",
    'th': "Thai",
    'ru': "Russian",
    'pt': "Portuguese",
    'es': "Spanish",
    'hi': "Hindi",
    'tr': "Turkish",
    'ar': "Arabic",
}


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def call_api(text, system_prompt, image):
    
    base64_image = encode_image(image)
    response = openai.chat.completions.create(
        # model="模型",
        model = model_name, # 图文
        messages=[
            # {'role': 'system', 'content': system_prompt},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            # 需要注意，传入Base64，图像格式（即image/{format}）需要与支持的图片列表中的Content Type保持一致。"f"是字符串格式化的方法。
                            # PNG图像：  f"data:image/png;base64,{base64_image}"
                            # JPEG图像： f"data:image/jpeg;base64,{base64_image}"
                            # WEBP图像： f"data:image/webp;base64,{base64_image}"
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}, 
                        },
                        {"type": "text", "text": text},
                    ],
                }
        ],
    )
    return response.choices[0].message.content

PROMPT = """
Task Description:
You will be given an e-commerce promotional image (which may contain Chinese and English text) along with a manually extracted Chinese text list. 
Your job is to translate ONLY the provided Chinese text into {tgt_lang}. 
DO NOT extract or translate any additional text from the image itself. 
The image is only provided to help you understand the visual style, brand tone, and marketing context.

Translation Requirements:
1. Translate only the provided Chinese text. Do not add, omit, or modify content beyond translation.
2. The translation should fit the context of e-commerce advertising — fluent, natural, and persuasive.
3. Preserve brand names and product names as-is or transliterate naturally.
4. Tone: concise, appealing, and appropriate for product promotional images.
5. Brand names may be retained in their original names.

Output Format:
Return the result strictly as a valid JSON object, where each key is the original Chinese text, and each value is its {tgt_lang} translation.
Do not include any explanations, comments, or extra text outside the JSON.

Example Output:

{{
  "3·8抢先购": "3.8 Early Access Sale",
  "浅野": "浅野",
  "海外旗舰店": "Overseas Flagship Store"
}}

Chinese Text:
{zh_text}
"""


def process(ref, image_folder, tgt_l="en", retries=3, retry_wait=2):
    data = json.load(open(ref, 'r', encoding="utf-8"))
    print(len(data))
    err_data = {}

    for k, v in tqdm.tqdm(data.items()):
        zh = v["zh"]
        prompt = PROMPT.format(
            tgt_lang=lang_map[tgt_l],
            zh_text="\n".join(zh)
        )
        image = image_folder + k
        last_error = None  

        for attempt in range(1, retries + 1):
            try:
                outputs = call_api(prompt, None, image)
                # outputs = prompt
                break   # 成功 → 跳出重试循环
            except Exception as e:
                last_error = str(e)  # 记录最后一次错误
                print(f"[{k}] 第 {attempt} 次失败：{e}")
                if attempt < retries:
                    time.sleep(retry_wait)
                else:
                    print(f"[{k}] 已重试 {retries} 次仍失败 → 写入空结果")
                    outputs = ""
                    # === 记录错误到 error_log.json ===
                    err_data[image]= last_error

        v[tgt_l] = outputs

    output_path = os.path.join(root, f"{model_name}_translate_{tgt_l}.json")
    print(f"Saving results to: {output_path}")
    json.dump(data, open(output_path, 'w', encoding="utf-8"), ensure_ascii=False, indent=4)
    if len(err_data) > 0:
        error_log_path = os.path.join(root, f"{model_name}_translate_{tgt_l}_error_log.json")
        json.dump(err_data, open(error_log_path, 'w'), ensure_ascii=False, indent=4)



if __name__ == '__main__':


    # 使用用户输入的模型名
    model_name = "gpt-5-2025-08-07-GlobalStandard"
    print(f"Using model: {model_name}", "target language: {tgt_lang}")

    error_file = {}
    root = f"/mnt/workspace/xintong/pjh/All_result/alitrans_translate_results/find_empty/"

    today=datetime.date.today()

    Path(root).mkdir(parents=True, exist_ok=True)
    print("路径保存地址在", root)
    image_folder = "/mnt/workspace/xintong/dataset/practice_ds_500/"


    for file in Path("empty").rglob("*.json"):
        tgt_lang = file.stem.split("_")[-1]
        print("file ", file)
        process(file, image_folder, tgt_lang)