FROM python:3.9.5-slim-buster
ENV PYTHONUNBUFFERED 1
WORKDIR /order_service
COPY requirements.txt /order_service
RUN pip install -r requirements.txt
COPY . /order_service
RUN chmod +x /order_service/entrypoint.sh
ENTRYPOINT ["/order_service/entrypoint.sh"]