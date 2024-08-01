FROM python:3.12

ENV HF_HOME=huggingface

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN addgroup --gid 200 --system app && adduser --uid 200 --gid 200 --home /app app
WORKDIR /app
USER app

COPY --chown=200:200 src src
RUN python src/download.py

ENV HF_DATASETS_OFFLINE=1
ENV HF_HUB_OFFLINE=1
EXPOSE 8000
CMD ["python", "src/run.py"]
