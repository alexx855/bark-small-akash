FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

ENV GRADIO_SERVER_PORT=7860
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV SHARE_INTERFACE=True
ENV OUTPUT_DIR=/mnt/output

WORKDIR /opt/app

# Copy requirements first for better caching
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y git && \
    pip install -r requirements.txt

# Create mount point and set permissions
RUN mkdir -p /mnt && \
    chmod 777 /mnt

# Copy application files
COPY main.py .
COPY app.py .

# Create volume mount point
VOLUME /mnt

# Run the Gradio app
CMD ["python", "app.py"]