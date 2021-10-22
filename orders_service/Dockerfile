FROM python:3.9.5-slim-buster
ENV PYTHONUNBUFFERED 1
WORKDIR /orders_service
COPY requirements.txt /orders_service
RUN pip install -r requirements.txt
COPY . /orders_service
RUN chmod +x /orders_service/entrypoint.sh
ENTRYPOINT ["/orders_service/entrypoint.sh"]