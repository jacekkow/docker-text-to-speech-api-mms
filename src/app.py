import io

import fastapi
import pydantic
import scipy
import transformers
import torch

from config import *

tokenizers = {}
models = {}

for lang in LanguageModel:
	tokenizers[lang.value] = transformers.AutoTokenizer.from_pretrained('./data/tokenizer/facebook/mms-tts-' + lang.name)
	models[lang.value] = transformers.VitsModel.from_pretrained('./data/model/facebook/mms-tts-' + lang.name)


class SynthesizeRequest(pydantic.BaseModel):
	language: LanguageModel
	text: str

class SynthesizeResponse(fastapi.Response):
	media_type = 'audio/wav'


app = fastapi.FastAPI()


@app.post('/synthesize', response_class=SynthesizeResponse)
async def synthesize(request: SynthesizeRequest) -> SynthesizeResponse:
	inputs = tokenizers[request.language.value](request.text, return_tensors='pt')
	model = models[request.language.value]
	with torch.no_grad():
		output = model(**inputs).waveform

	with io.BytesIO() as fp:
		scipy.io.wavfile.write(fp, rate=model.config.sampling_rate, data=output.float().numpy().T)
		return SynthesizeResponse(content = fp.getvalue())
