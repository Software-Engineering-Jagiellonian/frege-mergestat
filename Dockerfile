FROM golang:1.17-buster as builder
WORKDIR /app
RUN apt-get update && apt-get -y install cmake libssl-dev
COPY mergestat/. .
RUN make libgit2
RUN make

FROM debian:buster-slim as mergestat
WORKDIR /app/
RUN mkdir /repo
COPY --from=builder /app/.build/mergestat .
RUN apt-get update && apt-get install -y git
#ENTRYPOINT ["./mergestat", "--repo", "/repo"]

FROM python:3.9 as backend
WORKDIR /app
COPY --from=mergestat /app .
WORKDIR /backend
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./main.py /backend/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
