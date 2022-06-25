FROM python:3.10

WORKDIR /backend
COPY /backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT [ "/bin/bash" ]
