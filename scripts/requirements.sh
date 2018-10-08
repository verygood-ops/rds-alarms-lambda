#!/usr/bin/env bash
# Because "install -r requirements.txt" does not have "-t"
mkdir -p vendor
pip2 install psycopg2-binary -t `pwd`/vendor
pip2 install records -t `pwd`/vendor
