from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

save_path = "./models/nllb-200"

# 下载并保存
tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")

tokenizer.save_pretrained(save_path)
model.save_pretrained(save_path)

print("模型保存完毕！")
