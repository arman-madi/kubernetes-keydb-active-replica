FROM python:alpine3.12
LABEL author="https://www.linkedin.com/in/armanmadi/"
LABEL github="https://github.com/arman-madi/kubernetes-keydb-active-replica"

RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/
CMD ["python", "/app/main.py"]