FROM python:3
WORKDIR /usr/src/app
COPY uca/ uca/
COPY requirements.txt setup.py README.md ./
RUN python3 setup.py install
CMD ["uca/main.py"]
ENTRYPOINT ["python3"]
