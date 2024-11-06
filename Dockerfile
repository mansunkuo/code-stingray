FROM python:3.12-slim-bookworm

WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENTRYPOINT ["python"]
CMD ["-m", "code_stingray.cli", "-h"]