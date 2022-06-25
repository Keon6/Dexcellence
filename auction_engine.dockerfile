FROM python:3.10

WORKDIR /backend
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]