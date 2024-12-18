FROM python:3.9.12-alpine3.15
EXPOSE 5000

# instalando o que meu projeto precisa para rodar
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY wsgi.py .
COPY config.py .
COPY application application
 
CMD [ "python", "wsgi.py" ]