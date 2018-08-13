FROM python:3.6
ADD . /home/py
WORKDIR /home/py
COPY ./scrapyd.conf /etc/scrapyd/
EXPOSE 6800
RUN pip3 install -r requirements.txt
CMD scrapyd
