FROM python:3.12-slim

RUN mkdir /app \
    && chown -R 888 /app \
    && pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu \
    && pip install seldon-core==1.18.2 sentence_transformers==3.2.1 optimum-intel==1.20.0 openvino

ADD *.py /app
WORKDIR /app

CMD exec seldon-core-microservice run_ov --service-type MODEL
