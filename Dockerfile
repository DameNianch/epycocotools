FROM python:3.12.3-bullseye

RUN pip install numpy cython pytest

WORKDIR /workspace
