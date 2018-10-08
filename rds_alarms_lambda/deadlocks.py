from rds_alarms_lambda.lib import db, DB_NAME, every_minute, RDSLambdaAlert
import logging

log = logging.getLogger(__name__)


@every_minute
def longer_than_1_min():
    query = """
    SELECT now() - query_start as "runtime",
        usename,
        datname,
        wait_event_type,
        wait_event,
        state,
        query
    FROM  pg_stat_activity
    WHERE now() - query_start > '1 minutes'::interval
        AND state='idle'
        AND wait_event IS NOT NULL
        AND datname='{}'
    ORDER BY runtime DESC;
    """.format(DB_NAME)
    rows = db.query(query).export('csv')
    if rows:
        msg = "Found waiting RDS queries which exist more than 1 minute " \
              "already. Check RdsLambdaAlarms log for details."
        log.info(msg)
        log.info(rows)
        raise RDSLambdaAlert(msg)


@every_minute
def pg_deadlocks():
    query = "SELECT deadlocks FROM pg_stat_database WHERE datname='{}';".format(DB_NAME)
    rows = db.query(query)
    deadlocks = rows[0]['deadlocks']
    if deadlocks > 0:
        msg = "Query {} found {} deadlocks.".format(query, deadlocks)
        log.info(msg)
        raise RDSLambdaAlert(msg)


@every_minute
def pending_locks():
    query = """
    SELECT t.schemaname,
           t.relname,
           l.locktype,
           l.pid,
           l.mode,
           l.granted,
           now() - query_start AS "runtime",
           a.wait_event_type,
           a.wait_event,
           a.state,
           a.query
    FROM pg_locks l,
         pg_stat_all_tables t,
         pg_stat_activity a
    WHERE l.relation=t.relid
      AND a.pid=l.pid
      AND a.wait_event IS NOT NULL
      AND now() - query_start > '10 seconds'::interval
    ORDER BY runtime DESC;
    """
    rows = db.query(query).export('csv')
    if rows:
        msg = "Found RDS locks which are waiting more than 10 seconds " \
              "already. Check RdsLambdaAlarms log for details."
        log.info(msg)
        log.info(rows)
        raise RDSLambdaAlert(msg)
