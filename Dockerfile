FROM python:3.10-alpine

WORKDIR /splitwise-be

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "splitwise_pro.wsgi:application", "--reload", "--bind", "0.0.0.0:8000"]
