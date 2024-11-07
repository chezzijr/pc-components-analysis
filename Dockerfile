FROM python:3.12-alpine
WORKDIR /app
COPY . .
RUN python -m venv .venv \
    && source .venv/bin/activate \
    && pip install -r requirements.txt
CMD [".venv/bin/python", "main.py"]
