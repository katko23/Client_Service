FROM python:alpine

WORKDIR /app

COPY . .

EXPOSE 27002

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python" , "ClientServiceMain.py"]