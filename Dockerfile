FROM python:3.12-slim

RUN mkdir /app \
    && chown -R 888 /app \
    && mkdir /model \
    && chown -R 888 /model \
    && pip install seldon-core==1.18.2 sentence_transformers==3.2.1 optimum-intel==1.20.0 openvino \

ADD convert_to_ov.py run_st.py run_ov.py queries.py /app
ADD model/ /model

CMD exec seldon-core-microservice run_ov --service_type MODEL
