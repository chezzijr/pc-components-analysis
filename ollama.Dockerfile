FROM ollama/ollama

RUN ollama serve \
    & sleep 5 \
    && ollama pull nomic-embed-text \
    && ollama pull llama3.2:1b \
    && pkill ollama

EXPOSE 11434
ENTRYPOINT ["ollama", "serve"]
