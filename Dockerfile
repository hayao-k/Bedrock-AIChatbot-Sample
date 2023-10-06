FROM python:3.11-slim
WORKDIR /app

RUN useradd -m bedrock && chown -R bedrock /app
USER bedrock
ENV PATH="/home/bedrock/.local/bin:${PATH}"

COPY --chown=bedrock:bedrock app.py prompt_template.py chainlit.md /app/
COPY --chown=bedrock:bedrock requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

CMD ["chainlit", "run", "app.py"]