FROM python:3.9-slim
WORKDIR /src
COPY src /src
COPY ./requirements.txt /src
RUN pip install --no-cache-dir -r requirements.txt
VOLUME /src/output
CMD ["python", "cmd.py", "--url", "https://pouyae.ir", "--exact", "--output", "/src/output"]


# docker build -t crawler .
# docker run -v /Users/null/Desktop/code:/src/output --name crawler crawler
