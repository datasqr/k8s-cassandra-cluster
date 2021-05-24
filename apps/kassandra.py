import os
import json

from cassandra.cluster import Cluster, Session, ResponseFuture
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import ConstantReconnectionPolicy

CASSANDRA_HOSTS = os.getenv("CASSANDRA_HOSTS", "0.0.0.0").split(",")
CASSANDRA_PORT = os.getenv("CASSANDRA_PORT", "9042")
CASSANDRA_USERNAME = os.getenv("CASSANDRA_USERNAME", "cassandra")
CASSANDRA_PASSWORD = os.getenv("CASSANDRA_PASSWORD", "cassandra")

CONCURRENCY_LEVEL = 32
TOTAL_QUERIES = 10000


def get_name_spaces(session: Session):
    rows = session.execute("DESCRIBE keyspaces")
    for row in rows:
        print(row)

def get_session() -> Cluster:
    auth = PlainTextAuthProvider(
        username=CASSANDRA_USERNAME, password=CASSANDRA_PASSWORD
    )
    rp = ConstantReconnectionPolicy(5, max_attempts=None)
    cluster = Cluster(
        contact_points=CASSANDRA_HOSTS,
        port=CASSANDRA_PORT,
        auth_provider=auth,
        reconnection_policy=rp,
    )
    
    return cluster


def initialize_keyspace(session: Session, name: str, replication: int = 1):
    session.execute(
        (
            f"CREATE KEYSPACE IF NOT EXISTS {name} "
            "WITH replication = "
            f"{{'class': 'SimpleStrategy', 'replication_factor': '{replication}'}}"
        )
    )


# def initialize_measurements_table(session: Session, keyspace: str, table: str):
#     session.execute(
#         (
#             f"CREATE TABLE IF NOT EXISTS {keyspace}.{table} "
#             "(name text, timestamp timestamp, value double, "
#             "PRIMARY KEY (name, timestamp)) "
#             "WITH CLUSTERING ORDER BY (timestamp DESC)"
#         )
#     )


# def async_data_insert(
#     session: Session, keyspace: str, table: str, measurement: Measurement
# ) -> ResponseFuture:
#     prepared_statement = session.prepare(
#         f"INSERT INTO {keyspace}.{table} (name, timestamp, value) VALUES (?, ?, ?)"
#     )
#     # parse date into datetime instance with timezone info
#     timestamp = dateutil.parser.isoparse(measurement.timestamp)
#     return session.execute_async(
#         prepared_statement, (measurement.name, timestamp, measurement.value)
#     )


if __name__ == "__main__":

    ###
    # CASSANDRA
    cluster = get_session()
    session = cluster.connect()
    initialize_keyspace(session, "test", 1)
    print(cluster.metadata.keyspaces)

    # initialize db in case keyspace and table do not exist
    # we use kafka consumer group to specify keyspace and table
    
    #get_name_spaces(session)
