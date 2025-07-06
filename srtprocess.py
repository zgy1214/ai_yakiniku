import copy
import pysrt
from datetime import timedelta

def merge_srt_list(srt_list, offset_seconds_list=None):
    """
    合并多个 pysrt 字幕对象为一个。

    参数:
        srt_list: List[pysrt.SubRipFile] — 要合并的字幕对象列表
        offset_seconds_list: List[float] or None — 每个字幕对象的时间偏移（秒）

    返回:
        pysrt.SubRipFile — 合并后的字幕对象
    """
    merged = pysrt.SubRipFile()
    current_index = 1

    for i, srt in enumerate(srt_list):
        # 时间偏移
        offset = offset_seconds_list[i] if offset_seconds_list else 0
        srt_cpy = copy.deepcopy(srt)
        if offset:
            srt_cpy.shift(seconds=offset)

        for sub in srt_cpy:
            sub.index = current_index
            merged.append(sub)
            current_index += 1

    return merged


def whisper_result_to_srt(result):
    """
    将 Whisper 的转录结果转换为 pysrt.SubRipFile 对象

    参数:
        result (dict): Whisper 的转录结果字典，需包含 'segments' 字段

    返回:
        pysrt.SubRipFile: 包含所有字幕条目的 SRT 对象
    """
    subs = pysrt.SubRipFile()

    for i, segment in enumerate(result['segments'], start=1):
        # 创建字幕条目
        sub = pysrt.SubRipItem(
            index=i,
            start=pysrt.SubRipTime(seconds=segment['start']),
            end=pysrt.SubRipTime(seconds=segment['end']),
            text=segment['text'].strip()
        )
        subs.append(sub)

    return subs


def save_srt_to_file(srt_object, output_path, encoding='utf-8'):
    """
    将 SRT 对象保存到文件

    参数:
        subs (pysrt.SubRipFile): SRT 字幕对象
        output_path (str): 输出文件路径
        encoding (str): 文件编码，默认为 'utf-8'
    """

    srt_object.save(output_path, encoding=encoding)


def format_ass_timestamp(t):
    """
    将pysrt的时间对象格式化为ASS字幕时间格式 (h:mm:ss.cs)
    """
    h = int(t.hours)
    m = int(t.minutes)
    s = int(t.seconds)
    cs = int(t.milliseconds / 10)  # centiseconds
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def srt_to_ass(srt_obj, output_path="output.ass"):
    """
    将SRT字幕对象转换为ASS字幕文件

    参数:
        srt_obj (pysrt.SubRipFile): 输入的pysrt对象
        output_path (str): 输出ASS文件路径
    """
    # ASS头部
    header = """[Script Info]
ScriptType: v4.00+
Collisions: Normal

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, 
StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,微软雅黑,60,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,0,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    # 字幕事件
    events = ""
    for sub in srt_obj:
        start = format_ass_timestamp(sub.start)
        end = format_ass_timestamp(sub.end)
        text = sub.text.replace('\n', '\\N')
        events += f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n"

    # 写入文件
    with open(output_path, "w", encoding="utf-8-sig") as f:
        f.write(header + events)

    print(f"ASS字幕文件已生成：{output_path}")


if __name__ == '__main__':
    srt = pysrt.open('test.srt', encoding='utf-8')
    srt_to_ass(srt, 'test_output.ass')

