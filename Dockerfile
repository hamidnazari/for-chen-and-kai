FROM python:3-alpine

ARG GIT_COMMIT_HASH

WORKDIR /app

COPY src/ /app/
COPY requirements.txt /app/

RUN pip3 install -Ur requirements.txt

ENV GIT_COMMIT_HASH=${GIT_COMMIT_HASH}

ENTRYPOINT ["python3", "cli.py", "--server"]
