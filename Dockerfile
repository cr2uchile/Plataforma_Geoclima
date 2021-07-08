FROM python:3.8.0-buster

WORKDIR /App

COPY . .

COPY requirements.txt .
COPY * ./
RUN pip install -r requirements.txt

#COPY . App/ 

EXPOSE 8051

CMD ["python","/App/aplicacion.py"]

