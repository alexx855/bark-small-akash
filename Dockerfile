FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

ENV GRADIO_SERVER_PORT=7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

WORKDIR /opt/app
COPY  requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY main.py main.py

ENTRYPOINT ["python", "main.py"]