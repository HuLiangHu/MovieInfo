FROM python:3.6
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' >/etc/timezone
COPY . /home/spiders
WORKDIR /home/spiders
RUN pip install -r requirements.txt
#Install Cron
#RUN apt-get update
#RUN apt-get -y install cron
#RUN  crontab /home/spiders/crontabfile
ENV APPNAME=scrapy
#复制crontabfile到/etc/crontab
#RUN cp /home/spiders/crontabfile /etc/crontab
#RUN touch /var/log/cron.log

# Run the command on container startup
#CMD cron && tail -f /var/log/cron.log
CMD python run.py
