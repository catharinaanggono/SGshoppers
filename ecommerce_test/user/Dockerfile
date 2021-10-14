FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /user_service
COPY requirements.txt /user_service
RUN pip install -r requirements.txt
COPY . /user_service
ENTRYPOINT ["python"]
CMD [ "/user_service/user.py"]