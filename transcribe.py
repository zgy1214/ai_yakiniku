import time

import torch
import whisper
from pydub import AudioSegment
from srtprocess import whisper_result_to_srt, save_srt_to_file

result_container = {}
def save_transcribe_to_srt(result):
    # 保存为SRT文件
    if result and 'segments' in result:
        try:
            subs = whisper_result_to_srt(result)

            # 打印前3条字幕示例
            print("\n前3条字幕示例:")

            for i in range(min(3, len(subs))):
                print(f"{subs[i].index}")
                print(f"{subs[i].start} --> {subs[i].end}")
                print(f"{subs[i].text}\n")
            save_srt_to_file(subs)
        except Exception as e:
            print(f"保存SRT文件时出错: {str(e)}")
    else:
        print("\n转录失败，未生成有效结果")

def transcribe(model,audio_file):

    print(f"\n开始转录音频: {audio_file}")
    print("语言设定为日语 (ja)")

    # 转录开始计时
    transcribe_start = time.time()
    result_container['result'] = model.transcribe(audio_file, language="ja", verbose=False, fp16=True,
                                        )

    # 转录完成
    transcribe_time = time.time() - transcribe_start
    print(f"\n转录完成，耗时: {transcribe_time:.2f}秒")
    return result_container.get('result', None)