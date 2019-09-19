FROM docker.io/centos:7

RUN yum makecache \
    && yum install -y make curl gcc zlib* openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel

COPY Python-3.6.3.tgz /home/Python-3.6.3.tgz
COPY get-pip.py /home/get-pip.py

RUN tar xzf /home/Python-3.6.3.tgz -C /tmp \
    && rm -f Python-3.6.3.tgz \
    && cd /tmp/Python-3.6.3/ \
    && ./configure --enable-shared --prefix=/usr/local \
    && make \
    && make altinstall \
    && ln -s /usr/local/bin/pip3.6 /usr/bin/pip3 \
    && ln -s /usr/local/bin/python3.6 /usr/bin/python3 \
    && rm -rf /tmp/Python-3.6.3 \
    && cd - \
    && echo "/usr/local/lib/" >> /etc/ld.so.conf.d/python3.6.3.conf \
    && ldconfig \
    && python3 /home/get-pip.py

COPY dockerlab /home/dockerlab

RUN pip install -r /home/dockerlab/requirements.txt

EXPOSE 8087

CMD python3 /home/dockerlab/main.py
