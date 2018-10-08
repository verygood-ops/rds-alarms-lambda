## RDS Lambda Alarms

A set of periodic RDS queries for RDS DB.

See [deadlocks.py](rds_alarms_lambda/deadlocks.py) for reference. 
Availbale execution periods:
 - every_minute
 - every_five_minutes
 - every_ten_minutes
 - every_hour
 - every_day

## Updating python dependencies

1. Update [requirements.sh](./scripts/requirements.sh)
2. `rm -rf ./vendor`
3. `./scripts/requirements.sh`

## Release Process

Code is packaged via docker to ensure compatibility with AWS Lambda runtime.
The `./vendor` dir is rebuilt inside the container every time. 
See [Dockerfile](./Dockerfile.package)

```bash
./scripts/package.sh
./scripts/stage.sh dev|prod
```