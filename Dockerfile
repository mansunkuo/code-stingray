FROM python:3.12-slim-bookworm

WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y --no-install-recommends git=1:2.39.5-0+deb12u1  && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app

ENTRYPOINT ["python"]
CMD ["-m", "code_stingray.cli", "-h"]