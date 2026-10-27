FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git less file && rm -rf /var/lib/apt/lists/* \
 && pip install --no-cache-dir openpyxl==3.1.5 \
 && useradd -m -s /bin/bash assistant \
 && mkdir -p /world && chmod 755 /world
WORKDIR /home/assistant
CMD ["tail", "-f", "/dev/null"]
