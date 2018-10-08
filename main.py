import os
import sys
import logging
# Make sure ./vendor is visible
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/vendor")

from rds_alarms_lambda.lib import ALL_CHECKS, RDSLambdaAlert, sns_alert
import rds_alarms_lambda.deadlocks  # Register deadlock checks


log = logging.getLogger(__name__)


def main(event, context):
    for check in ALL_CHECKS:
        try:
            check()
        except RDSLambdaAlert as e:
            sns_alert(msg=str(e))
        except Exception as e:
            msg = "Unexpected error in RDS alarms " \
                  "lambda:\n{}".format(repr(e))
            log.error(msg)
            sns_alert(msg=msg)
            break


if __name__ == "__main__":
    main(None, None)
