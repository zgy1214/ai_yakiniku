import time

import torch
import whisper
from pydub import AudioSegment
from srtprocess import whisper_result_to_srt, save_srt_to_file

result_container = {}

def transcribe(model,audio_file):

    print(f"\n开始转录音频: {audio_file}")
    print("语言设定为日语 (ja)")

    # 转录开始计时
    transcribe_start = time.time()
    result_container['result'] = model.transcribe(audio_file, language="ja", verbose=False, fp16=True,)

    # 转录完成
    transcribe_time = time.time() - transcribe_start
    print(f"\n转录完成，耗时: {transcribe_time:.2f}秒")
    raw_result = result_container.get('result', None)
    return whisper_result_to_srt(raw_result)