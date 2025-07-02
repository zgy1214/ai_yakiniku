from pydub import AudioSegment
import os
from pathlib import Path


def slice_audio(input_path, output_dir, slice_length_min=10):
    # 加载音频
    audio = AudioSegment.from_wav(input_path)
    duration_ms = len(audio)

    # 切片时长（毫秒）
    slice_len_ms = slice_length_min * 60 * 1000

    # 创建输出目录
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    num_slices = (duration_ms + slice_len_ms - 1) // slice_len_ms
    print(f"开始切片，总长度 {duration_ms / 60000:.2f} 分钟，共 {num_slices} 片段")

    slice_cnt = 0
    for i in range(num_slices):
        start = i * slice_len_ms
        end = min(start + slice_len_ms, duration_ms)
        segment = audio[start:end]
        output_file = output_dir / f"vocals_part{i + 1:03}.wav"
        segment.export(output_file, format="wav")
        print(f"切片保存: {output_file}")
        slice_cnt = slice_cnt + 1

    print("切片完成！")
    return slice_cnt
