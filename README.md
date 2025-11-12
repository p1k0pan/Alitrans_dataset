# Alib_dataset

## 2025年11月8日
对Alitrans数据集中剩下的数据，用GPT-5进行翻译

1. 第一步下载图片，直接运行： `bash data.sh`
2. 确认图片的文件夹位置在：`/mnt/workspace/xintong/dataset/practice_ds_500/`

3. 6个语言，需要用6个terminal分别运行运行：
- `python api_gpt5_translate.py --lang en`
- `python api_gpt5_translate.py --lang hi`
- `python api_gpt5_translate.py --lang de`
- `python api_gpt5_translate.py --lang ru`
- `python api_gpt5_translate.py --lang es`
- `python api_gpt5_translate.py --lang ar`

4. 保存结果位置：
`/mnt/workspace/xintong/pjh/All_result/alitrans_translate_results/`。一共6个文件打包
