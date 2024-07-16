FROM python:3.12.4

WORKDIR /python/app

RUN apt-get update && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost:8000/ || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

