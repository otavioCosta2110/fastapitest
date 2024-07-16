FROM python:3.9-alpine

WORKDIR /python/app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN addgroup -S appuser && adduser -S appuser -G appuser
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost:8000/ || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

