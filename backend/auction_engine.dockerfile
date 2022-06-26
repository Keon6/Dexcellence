FROM python:3.10

WORKDIR /backend
COPY /backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY /backend/start_engine.sh start_engine.sh
COPY /backend/start_web_server.sh start_web_server.sh
RUN ["chmod", "+x", "start_engine.sh"]
RUN ["chmod", "+x", "start_web_server.sh"]

# Start the auction engine
ENTRYPOINT [ "/bin/bash" ]
