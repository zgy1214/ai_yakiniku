import argparse
import time

import requests
import torch
import whisper

from check import check
from cut import slice_audio
from separate import separate_audio
from srtprocess import whisper_result_to_srt, save_srt_to_file, merge_srt_list, srt_to_ass
from transcribe import transcribe
from translate import translate_bilingual

# 音频文件路径

parser = argparse.ArgumentParser(description='命令行参数选项限制示例')

parser.add_argument(
    '-m',
    default='large-v2',
    help='模型'
)

parser.add_argument(
    '-b',
    default='',
    help='节目的id'
)

parser.add_argument(
    '-a',
    required=True,
    help='音频的文件名，必须在input目录下'
)

parser.add_argument(
    '-l',
    default='bi',
    choices=['bi', 'jp', 'cn'],
    help='目标语言，bi=中日双语，jp=只生成日语，cn=只生成中文'
)

# 解析参数
args = parser.parse_args()
bangumi_name = args.b
audio_name = args.a
audio_file = f"./input/{audio_name}"
language = args.l
model = args.m

try:
    response = requests.get(f'http://47.114.217.240:8000/metadatas/{bangumi_name}')
    print(f'节目名：{response.json()["name"]}')
except Exception as e:
    print('没有节目信息')

print(f"导出语言：{language}")

# 配置中间文件路径
pipeline_dir = './pipeline'
vocal_wav = "./pipeline/vocals.wav"
output_japsrt_raw = "./pipeline/jap_raw.srt"

# 指定本地模型路径
model_path = f"models/whisper/{model}.pt"

# 提取人声并切片
separate_audio(audio_file, './pipeline')
slice_cnt = slice_audio(vocal_wav, './pipeline')

start_time = time.time()
try:
    # 检查GPU是否可用
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # device = "cpu"
    print(f"正在使用设备: {device}")
    model = whisper.load_model(model_path, device=device)
    load_time = time.time() - start_time
    print(f"模型加载成功！耗时: {load_time:.2f}秒")
except Exception as e:
    print(f"模型加载失败: {str(e)}")
    exit()

srt_objs = []
for i in range(slice_cnt):
    print(f"开始转录第 {i + 1} / {slice_cnt} 个片段")
    slice_file = pipeline_dir + f'/vocals_part{i + 1:03}.wav'

    whisper_result = transcribe(audio_file=slice_file, model=model)
    srt_obj = whisper_result_to_srt(whisper_result)
    srt_obj.save(f'/vocals_part{i + 1:03}.srt')
    srt_objs.append(srt_obj)

offset_list = []
for index, sub_item in enumerate(srt_objs):
    offset_seconds = index * 600
    offset_list.append(offset_seconds)

merged_srt_object = merge_srt_list(srt_objs, offset_list)
save_srt_to_file(merged_srt_object, output_japsrt_raw)  # 存档保存

corrected_srt_object = check(merged_srt_object, bangumi_name)
final_srt_object = translate_bilingual(corrected_srt_object, bangumi_name, language=language)
ass_doc = srt_to_ass(final_srt_object, './output/output.ass')
