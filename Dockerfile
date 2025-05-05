FROM python:3.12.3

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py

CMD ["python", "app.py"]
