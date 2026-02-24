FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends pandoc texlive-xetex texlive-fonts-recommended texlive-fonts-extra \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir .

ARG INSTALL_LLAMA=0
RUN if [ "$INSTALL_LLAMA" = "1" ]; then pip install --no-cache-dir ".[llama]"; fi

ENTRYPOINT ["mcp"]
