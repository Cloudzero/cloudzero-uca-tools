FROM python:3.11.1-slim
WORKDIR /usr/src/app
COPY uca/ uca/
COPY pyproject.toml README.md LICENSE ./
RUN pip3 install -e .
ENTRYPOINT ["uca"]
