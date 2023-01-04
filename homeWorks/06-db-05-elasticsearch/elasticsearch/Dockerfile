FROM --platform=linux/x86_64 centos:7

ENV NODE_NAME=netology_test
ENV DISCOVERY_TYPE=single-node
ENV ES_HEAP_SIZE=262144

RUN yum install wget -y
RUN yum install perl-Digest-SHA -y

RUN wget https://fossies.org/linux/www/elasticsearch-8.5.3-linux-x86_64.tar.gz
#RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.5.3-linux-x86_64.tar.gz.sha512
#RUN shasum -a 512 -c elasticsearch-8.5.3-linux-x86_64.tar.gz.sha512 
RUN tar -xzf elasticsearch-8.5.3-linux-x86_64.tar.gz
RUN groupadd elasticsearch
RUN useradd elasticsearch -g elasticsearch -p elasticsearch
RUN chown -R elasticsearch:elasticsearch ./elasticsearch-8.5.3
RUN chmod o+x -R  ./elasticsearch-8.5.3
RUN chgrp elasticsearch ./elasticsearch-8.5.3/
RUN cd elasticsearch-8.5.3

RUN mkdir -m 774 -p /var/lib/elasticsearch-data \
    && chown elasticsearch -R /var/lib/elasticsearch-data \
    && mkdir -m 774 -p /var/log/elasticsearch \
    && chown elasticsearch -R /var/log/elasticsearch \
    && mkdir -m 774 -p /usr/share/elasticsearch/snapshot \
    && chown elasticsearch -R /usr/share/elasticsearch/snapshot



#CMD [ "./bin/elasticsearch" ]