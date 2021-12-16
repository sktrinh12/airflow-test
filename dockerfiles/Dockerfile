FROM apache/airflow:2.1.0

ARG ORACLE_VERSION=11.2.0.4.0
ARG ORACLE_SHORT_VER=11204
ENV CLIENT_ZIP=instantclient-basiclite-linux.x64-${ORACLE_VERSION}.zip
ENV SDK_ZIP=instantclient-sdk-linux.x64-${ORACLE_VERSION}.zip
ENV ORACLE_HOME=/opt/oracle
ENV TNS_ADMIN ${ORACLE_HOME}/network/admin

WORKDIR ${ORACLE_HOME}
USER root
RUN apt-get update \
	&& apt-get -yq install unzip curl \
	&& apt-get clean
#RUN curl -LJOk "https://download.oracle.com/otn/linux/instantclient/${ORACLE_SHORT_VER}/${CLIENT_ZIP}"\
	#&& curl -LJOk "https://download.oracle.com/otn/linux/instantclient/${ORACLE_SHORT_VER}/${SDK_ZIP}"

#RUN mkdir -p ${ORACLE_HOME}
COPY dockerfiles/${CLIENT_ZIP} ${ORACLE_HOME}/${CLIENT_ZIP} 
COPY dockerfiles/${SDK_ZIP} ${ORACLE_HOME}/${SDK_ZIP} 
RUN unzip ${ORACLE_HOME}/${CLIENT_ZIP} && unzip ${ORACLE_HOME}/${SDK_ZIP} \
	&& rm -f *.zip
VOLUME ["${TNS_ADMIN}"]

RUN apt-get -yq install libaio1 \
	&& apt-get autoremove \ 
	&& apt-get clean \
	&& echo ${ORACLE_HOME} > /etc/ld.so.conf.d/oracle.conf \
	&& mkdir -p ${TNS_ADMIN} \
	&& ldconfig \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install --no-cache-dir apache-airflow-providers-oracle

USER 50000
