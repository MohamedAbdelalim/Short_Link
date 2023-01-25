FROM python:3.11-alpine
LABEL maintainer="Mohamed Abdelalim"


WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
