FROM python:3.11

WORKDIR /sistem-monitoring
ADD . /sistem-monitoring

RUN pip install -r requirements.txt
RUN pip install mysql-connector
CMD [ "flask", 'run' ]