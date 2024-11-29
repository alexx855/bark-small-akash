FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

ENV GRADIO_SERVER_PORT=7860
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV SHARE_INTERFACE=True

WORKDIR /opt/app

# Copy requirements first for better caching
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Create output directory
RUN mkdir output

# Copy application files
COPY main.py .
COPY app.py .

# Run the Gradio app
CMD ["python", "app.py"]
