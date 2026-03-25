FROM apache/spark:3.4.2

USER root

# Installer Java 11
RUN apt-get update && apt-get install -y openjdk-11-jdk curl \
    && rm -rf /var/lib/apt/lists/*

# Variables Java
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# JDBC PostgreSQL
COPY postgresql-42.6.2.jar /opt/spark/jars/

# Jobs Spark
COPY jobs/ /opt/spark/jobs/
WORKDIR /opt/spark/jobs

# Entrypoint
COPY spark-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 4040 7077 8080 8081

ENTRYPOINT ["/entrypoint.sh"]