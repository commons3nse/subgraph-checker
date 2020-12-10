FROM python:3.7

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
ENV PATH="$PATH:/root/.poetry/bin"
COPY pyproject.toml poetry.lock /app/
WORKDIR /app
RUN poetry install -n

COPY . /app

CMD ["poetry", "run", "python", "main.py"]