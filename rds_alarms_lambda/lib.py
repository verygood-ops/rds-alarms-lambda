import os
import records
import sys
import boto3
import datetime
import functools
import logging
import urlparse


DB_CONN_STRING = os.environ['DB_CONN_STRING']
DB_NAME = urlparse.urlparse(DB_CONN_STRING).path.lstrip("/")
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

THIS_HOUR = datetime.datetime.now().hour
THIS_MINUTE = datetime.datetime.now().minute

log = logging.getLogger()
if log.handlers:  # Hack AWS logging
    for handler in log.handlers:
        log.removeHandler(handler)
logging.basicConfig(stream=sys.stdout, format='%(asctime)s %(message)s',
                    level=logging.INFO)
logging.getLogger("botocore").setLevel(logging.ERROR)

log.info("Connecting database...")
db = records.Database(DB_CONN_STRING)
log.info("Connection established.")
sns = boto3.client('sns')


class RDSLambdaAlert(Exception):
    pass


def _logged_call(f, via):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        log.info("Invoking RDS check '{}' (via '{}')".format(f.__name__,
                                                             via.__name__))
        return f(*args, **kwargs)
    return wrapper


ALL_CHECKS = []


def every_minute(f):
    ALL_CHECKS.append(_logged_call(f, every_minute))
    return f


def every_five_minutes(f):
    if THIS_MINUTE % 5 == 0:
        ALL_CHECKS.append(_logged_call(f, every_five_minutes))
    return f


def every_ten_minutes(f):
    if THIS_MINUTE % 10 == 0:
        ALL_CHECKS.append(_logged_call(f, every_ten_minutes))
    return f


def every_hour(f):
    if THIS_MINUTE == 0:
        ALL_CHECKS.append(_logged_call(f, every_hour))
    return f


def every_day(f):
    if THIS_MINUTE == 0 and THIS_HOUR == 0:
        ALL_CHECKS.append(_logged_call(f, every_day))
    return f


def sns_alert(subj="RDS lambda alarm", msg=""):
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subj,
        Message=msg,
    )
