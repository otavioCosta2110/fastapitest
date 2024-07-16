FROM python:latest

WORKDIR /python/app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8000

CMD ["fastapi", "run", "./main.py"]

