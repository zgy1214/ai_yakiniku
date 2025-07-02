import pysrt
from check import check
from srtprocess import srt_to_ass
from translate import translate_bilingual

bangumi_name = "snb"  # 示例节目名称

if __name__ == '__main__':
    srt_path = './pipeline/jap_raw.srt'
    srt_obj = pysrt.open(srt_path, encoding='utf-8')

    corrected_srt_object = check(srt_obj, bangumi_name)

    final_srt_object = translate_bilingual(corrected_srt_object, bangumi_name)
    ass_doc = srt_to_ass(final_srt_object, './output/output.ass')
