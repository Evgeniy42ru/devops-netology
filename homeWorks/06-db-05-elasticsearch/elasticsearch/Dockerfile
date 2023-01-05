FROM centos:7

ENV ES_HEAP_SIZE=262144

RUN yum install wget -y
RUN yum install perl-Digest-SHA -y

RUN wget https://fossies.org/linux/www/elasticsearch-8.5.3-linux-x86_64.tar.gz
#RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.5.3-linux-x86_64.tar.gz.sha512
#RUN shasum -a 512 -c elasticsearch-8.5.3-linux-x86_64.tar.gz.sha512 
RUN tar -xzf elasticsearch-8.5.3-linux-x86_64.tar.gz

COPY ./elasticsearch.yml /elasticsearch-8.5.3/config/elasticsearch.yml

RUN groupadd elasticsearch

RUN useradd elasticsearch -g elasticsearch -p elasticsearch \
&& chown -R elasticsearch:elasticsearch ./elasticsearch-8.5.3 \
&& chmod o+x -R  ./elasticsearch-8.5.3

RUN mkdir -m 774 -p /var/lib/elasticsearch-data \
    && chown elasticsearch -R /var/lib/elasticsearch-data \
    && mkdir -m 774 -p /var/log/elasticsearch \
    && chown elasticsearch -R /var/log/elasticsearch \
    && mkdir -m 774 -p /elasticsearch-8.5.3/snapshot \
    && chown elasticsearch -R /elasticsearch-8.5.3/snapshot

RUN cd elasticsearch-8.5.3

#CMD [ "./bin/elasticsearch" ]