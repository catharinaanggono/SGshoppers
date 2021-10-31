FROM python:3.9.5-slim-buster
ENV PYTHONUNBUFFERED 1
WORKDIR /product_service
COPY requirements.txt /product_service
RUN pip install -r requirements.txt
COPY . /product_service
RUN chmod +x /product_service/entrypoint.sh
ENTRYPOINT ["/product_service/entrypoint.sh"]