from datetime import datetime
import os

import pysrt
import pysubs2
import whisper
from pydub import AudioSegment

from srtprocess import ass_to_pysrt, srt_to_ass
from transcribe import transcribe


def detect_and_fill_missing_subs(subs: pysrt.SubRipFile, audio_file: str, model ,threshold: float = 20.0 ) -> pysrt.SubRipFile:
    """
    检测字幕中的缺失部分并使用whisper补全
    :param subs: pysrt.SubRipFile 对象
    :param audio_file: 音频文件路径
    :param threshold: 缺失判断的时间阈值，单位：秒
    :return: 新的补全后的 pysrt.SubRipFile
    """
    new_subs = pysrt.SubRipFile(items=subs[:] if subs else [])
    inserts = []
    audio = AudioSegment.from_wav(audio_file)

    for i in range(len(subs) - 1):
        end_current = subs[i].end.to_time()
        start_next = subs[i + 1].start.to_time()
        gap = (datetime.combine(datetime.min, start_next) - datetime.combine(datetime.min, end_current)).total_seconds()

        if gap > threshold:
            print(f"[{end_current.strftime('%H:%M:%S')} - {start_next.strftime('%H:%M:%S')}] 可能缺失")

            start_sec = end_current.hour * 3600 + end_current.minute * 60 + end_current.second + end_current.microsecond / 1e6
            end_sec = start_next.hour * 3600 + start_next.minute * 60 + start_next.second + start_next.microsecond / 1e6

            # 切片并保存临时文件
            start_ms = int(start_sec * 1000)
            end_ms = int(end_sec * 1000)
            segment = audio[start_ms:end_ms]

            temp_filename = f"missing_{int(start_sec)}_{int(end_sec)}.wav"
            temp_path = os.path.join( "./pipeline", temp_filename)
            segment.export(temp_path, format="wav")

            missing_subs = transcribe(audio_file=temp_path, model=model)

            # 平移字幕时间
            for item in missing_subs:
                item.shift(seconds=start_sec)
                inserts.append(item)

            # 删除中间文件
            try:
                os.remove(temp_path)
                os.remove(temp_path + ".srt")
            except OSError:
                pass

    new_subs.extend(inserts)
    new_subs.sort()
    new_subs.clean_indexes()
    return new_subs

if __name__ == '__main__':
    model = whisper.load_model('./models/whisper/large-v2.pt', device='cuda') # 自动识别 .ass 格式
    pysrt_obj = ass_to_pysrt('snb.ass')
    pysrt_obj = detect_and_fill_missing_subs(pysrt_obj,'./pipeline/vocals.wav',model)
    srt_to_ass(pysrt_obj, 'test_output.ass')