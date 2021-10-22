FROM python:3.9.5-slim-buster
ENV PYTHONUNBUFFERED 1
WORKDIR /rewards_service
COPY requirements.txt /rewards_service
RUN pip install -r requirements.txt
COPY . /rewards_service
RUN chmod +x /rewards_service/entrypoint.sh
ENTRYPOINT ["/rewards_service/entrypoint.sh"]