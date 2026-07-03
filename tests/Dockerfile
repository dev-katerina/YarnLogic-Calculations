FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
COPY ./tests ./tests
COPY pytest.ini .
# CMD ["pytest", "-v", "--disable-warnings", "--maxfail=1"]
CMD ["pytest", "-m", "elastic", "-v", "--disable-warnings", "--maxfail=1"]