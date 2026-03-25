#!/bin/bash
# =============================================================================
# Spark – Entrypoint (Apache Spark officiel)
# =============================================================================
set -e

SPARK_HOME="/opt/spark"
export SPARK_CONF_DIR="${SPARK_HOME}/conf"
export PATH="${SPARK_HOME}/bin:${PATH}"

mkdir -p ${SPARK_CONF_DIR}

# -----------------------------------------------------------------------------
# spark-defaults.conf
# -----------------------------------------------------------------------------
cat > ${SPARK_CONF_DIR}/spark-defaults.conf <<EOF
spark.master                     spark://${SPARK_MASTER_HOST:-spark-master}:7077
spark.ui.showConsoleProgress     true
spark.driver.cores               2
spark.driver.memory              2g
spark.executor.cores             2
spark.executor.memory            2g
spark.sql.shuffle.partitions     4

# HDFS
# spark.hadoop.fs.defaultFS        hdfs://${NAMENODE_HOST:-namenode}:8020
# spark.hadoop.dfs.replication     2

# PostgreSQL JDBC
spark.jars                       /opt/spark/jars/postgresql-42.6.2.jar

# Event log
spark.eventLog.enabled           true
spark.eventLog.dir               /opt/spark/logs
EOF

# -----------------------------------------------------------------------------
# spark-env.sh
# -----------------------------------------------------------------------------
cat > ${SPARK_CONF_DIR}/spark-env.sh <<EOF
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export SPARK_HOME=${SPARK_HOME}
export SPARK_LOG_DIR=/opt/spark/logs
EOF

mkdir -p /opt/spark/logs

# -----------------------------------------------------------------------------
# Sélection du rôle
# -----------------------------------------------------------------------------
case "${SPARK_ROLE}" in
  master)
    echo "[Spark] Démarrage en mode MASTER"
    exec ${SPARK_HOME}/bin/spark-class \
      org.apache.spark.deploy.master.Master \
      --host 0.0.0.0 \
      --port 7077 \
      --webui-port 8080
    ;;
  worker)
    echo "[Spark] Démarrage en mode WORKER"
    exec ${SPARK_HOME}/bin/spark-class \
      org.apache.spark.deploy.worker.Worker \
      spark://${SPARK_MASTER_HOST:-spark-master}:${SPARK_MASTER_PORT:-7077} \
      --cores ${SPARK_WORKER_CORES:-2} \
      --memory ${SPARK_WORKER_MEMORY:-2g} \
      --webui-port 8081
    ;;
  submit)
    echo "[Spark] Mode SUBMIT"
    exec ${SPARK_HOME}/bin/spark-submit "$@"
    ;;
  *)
    echo "[ERREUR] SPARK_ROLE invalide : ${SPARK_ROLE}"
    exit 1
    ;;
esac