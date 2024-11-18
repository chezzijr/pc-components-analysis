FROM python:3.12.7-bookworm
WORKDIR /app
ARG STREAMLIT_PORT
COPY . .
RUN python -m venv .venv \
    && . .venv/bin/activate \
    && pip install -r requirements.txt
CMD .venv/bin/python -m streamlit run main.py --server.port $STREAMLIT_PORT
