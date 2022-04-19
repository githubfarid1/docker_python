FROM ubuntu:20.04
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV workdir /usr/project
WORKDIR ${workdir}

RUN pip install --upgrade pip
RUN pip install playwright
RUN playwright install
RUN pip install bs4
RUN playwright install-deps