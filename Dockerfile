FROM python:3.7
RUN mkdir -p /usr/src/dsandrewbot/
WORKDIR /usr/src/dsandrewbot/
RUN pip3 install discord
COPY . /usr/src/dsandrewbot/

CMD ["python", "DSBOT.py"]
