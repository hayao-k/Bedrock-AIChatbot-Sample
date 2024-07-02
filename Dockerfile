FROM python:3.12-slim
WORKDIR /app

RUN useradd -m bedrock && chown -R bedrock /app
USER bedrock
ENV PATH="/home/bedrock/.local/bin:${PATH}"

COPY --chown=bedrock:bedrock app.py chainlit*.md /app/
COPY --chown=bedrock:bedrock .chainlit/ /app/.chainlit/
COPY --chown=bedrock:bedrock requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

CMD ["chainlit", "run", "app.py"]