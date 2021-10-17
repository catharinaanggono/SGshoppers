FROM python:3.9.5-slim-buster
ENV PYTHONUNBUFFERED 1
WORKDIR /user_service
COPY requirements.txt /user_service
RUN pip install -r requirements.txt
COPY . /user_service
RUN chmod +x /user_service/entrypoint.sh
ENTRYPOINT ["/user_service/entrypoint.sh"]