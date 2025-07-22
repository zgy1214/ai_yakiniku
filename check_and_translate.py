import pysrt
from check import check
from srtprocess import srt_to_ass, ass_to_pysrt
from translate import translate_bilingual

bangumi_name = "hnstarinai_12"  # 示例节目名称
check = False

if __name__ == '__main__':
    #srt_obj = pysrt.open('./pipeline/jap_raw.srt', encoding='utf-8')
    srt_obj = ass_to_pysrt('output (3).ass')

    if check:
        srt_obj = check(srt_obj, bangumi_name)

    final_srt_object = translate_bilingual(srt_obj, bangumi_name, language='bi')
    ass_doc = srt_to_ass(final_srt_object, './output/output.ass')
