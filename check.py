import time

import pysrt

from llm import client, client_2
from prompts.prompt_jp import get_prompt_jp


def parse_corrected_text_to_srt(corrected_text, original_chunk):
    """将LLM返回的文本解析回pysrt格式，并替换原始chunk中的文本"""
    corrected_lines = corrected_text.strip().split('\n\n')
    corrected_subs = []
    for orig, corr in zip(original_chunk, corrected_lines):
        parts = corr.strip().split('\n')
        if len(parts) < 3:
            corrected_text = orig.text  # 如果格式异常则保留原文
        else:
            corrected_text = '\n'.join(parts[2:])  # 跳过index和时间轴
        new_sub = orig
        new_sub.text = corrected_text
        corrected_subs.append(new_sub)
    return corrected_subs

def srt_chunk_to_text(subs):
    """将一个srt字幕列表转为用于校对的纯文本表示"""
    return "\n\n".join(
        f"{sub.index}\n{sub.start} --> {sub.end}\n{sub.text}" for sub in subs
    )

def check(srt_obj,bangumi_name):
    corrected = []

    chunk_size = 60
    for i in range(0, len(srt_obj), chunk_size):
        chunk = srt_obj[i:i + chunk_size]
        content = srt_chunk_to_text(chunk)
        print(f" 校对中：第 {i + 1} 行 ～ 第 {min(i + chunk_size, len(srt_obj))} 行（全 {len(srt_obj)} 行中）")
        # 向LLM请求校对
        response = client_2.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {'role': 'system', 'content': get_prompt_jp(bangumi_name)},
                {"role": "user", "content": f"以下は字幕データです。すべての字幕行を必ず出力し、ルールに従って自然に校正してください：\n\n{content}"}
            ],
            stream=False
        )

        result_text = response.choices[0].message.content
        corrected_chunk = parse_corrected_text_to_srt(result_text, chunk)
        corrected.extend(corrected_chunk)

        # 控制节奏防止触发频率限制
        time.sleep(1)

    # 创建新srt对象
    corrected_srt = pysrt.SubRipFile(items=corrected)
    return corrected_srt


if __name__ == '__main__':
    #读取srt文件
    # 读取本地srt文件
    srt_path = './pipeline/jap_raw.srt'
    srt_obj = pysrt.open(srt_path, encoding='utf-8')

    bangumi_name = "yakouseijiron"  # 示例节目名称
    corrected_srt = check(srt_obj, bangumi_name)

    # 输出为新文件
    corrected_srt.save('corrected_example.srt', encoding='utf-8')