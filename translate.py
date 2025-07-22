import copy
import time

import pysrt

from llm import client_2
from prompts.prompt_zh import get_prompt_zh
from srtprocess import ass_to_pysrt, srt_to_ass


def parse_translated_text_to_srt(translated_text, original_chunk):
    """将LLM返回的翻译文本解析为pysrt格式，并替换原始chunk中的文本"""
    translated_lines = translated_text.strip().split('\n\n')
    translated_subs = []
    for orig, trans in zip(original_chunk, translated_lines):
        parts = trans.strip().split('\n')
        if len(parts) < 3:
            translated_text = orig.text  # 如果格式异常则保留原文
        else:
            translated_text = '\n'.join(parts[2:])  # 跳过index和时间轴
        new_sub = orig
        new_sub.text = translated_text
        translated_subs.append(new_sub)
    return translated_subs


def srt_chunk_to_text(subs):
    """将一个srt字幕列表转为纯文本格式，供LLM翻译"""
    return "\n\n".join(
        f"{sub.index}\n{sub.start} --> {sub.end}\n{sub.text}" for sub in subs
    )


def translate_bilingual(srt_obj, bangumi_name, language='bi'):
    if language == 'jp':
        return srt_obj  # 无需翻译
    translated = []
    chunk_size = 60

    for i in range(0, len(srt_obj), chunk_size):
        chunk = srt_obj[i:i + chunk_size]
        chunk_cpy = copy.deepcopy(chunk)
        content = srt_chunk_to_text(chunk)
        print(f"翻译中：第 {i + 1} 行 ～ 第 {min(i + chunk_size, len(srt_obj))} 行（共 {len(srt_obj)} 行）")

        # 调用翻译模型
        response = client_2.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {'role': 'system', 'content': get_prompt_zh(bangumi_name)},
                {'role': 'user', 'content': f"以下是字幕内容，请将每句翻译为中文，对应保留原句：\n\n{content}"}
            ],
            stream=False
        )

        # 获取中文翻译（逐句）

        result_text = response.choices[0].message.content
        translated_chunk = parse_translated_text_to_srt(result_text, chunk)

        for i, orig in enumerate(chunk_cpy):
            # 构建新字幕条目
            if language == 'bi':
                # 构建双语字幕
                trans_text = translated_chunk[i].text.strip() if i < len(translated_chunk) else ""
                new_sub = pysrt.SubRipItem(
                    index=orig.index,
                    start=orig.start,
                    end=orig.end,
                    text=f"{trans_text}\n{orig.text.strip()}" if trans_text else orig.text.strip()
                )
                translated.append(new_sub)
            else:
                # 单语模式
                if i < len(translated_chunk):
                    translated.append(translated_chunk[i])
                else:
                    # 保留原时间轴但内容为空
                    empty_sub = pysrt.SubRipItem(
                        index=orig.index,
                        start=orig.start,
                        end=orig.end,
                        text=""
                    )
                    translated.append(empty_sub)

        time.sleep(1)

    return pysrt.SubRipFile(items=translated)


if __name__ == '__main__':
    srt_obj = ass_to_pysrt('test_output.ass')

    bangumi_name = "snb"
    translated_srt = translate_bilingual(srt_obj, bangumi_name)

    srt_to_ass(translated_srt,'#1.ass')
