# RDS Alarms Lambda

A set of periodic RDS queries in a form of AWS Lambda.

#### Use cases
- Deadlock monitor. See [deadlocks.py](rds_alarms_lambda/deadlocks.py)
- DB healthcheck
- Schema consistency monitor
- Garbage Collection

#### Availbale execution periods
- `every_minute`
- `every_five_minutes`
- `every_ten_minutes`
- `every_hour`
- `every_day`

## Hacking

This code distributed under MIT. Pull requests welcome.

#### Updating python dependencies

1. Update [requirements.sh](./requirements.sh)
2. `rm -rf ./vendor`
3. `./requirements.sh`

#### Release process

Code is packaged via docker to ensure compatibility with AWS Lambda runtime.
The `./vendor` dir is rebuilt inside the container every time. 
See [Dockerfile](./Dockerfile.package)

```bash
./ops/package.sh
./ops/stage.sh dev|prod
```