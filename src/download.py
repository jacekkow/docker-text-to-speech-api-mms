import transformers

from config import LanguageModel

for lang in LanguageModel:
	tokenizer = transformers.AutoTokenizer.from_pretrained('facebook/mms-tts-' + lang.name)
	tokenizer.save_pretrained('./data/tokenizer/facebook/mms-tts-' + lang.name)
	model = transformers.VitsModel.from_pretrained('facebook/mms-tts-' + lang.name)
	model.save_pretrained('./data/model/facebook/mms-tts-' + lang.name)
